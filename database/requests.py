from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from database.models import ActionLog, Order, Price, User

# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------


async def get_or_create_user(
    session: AsyncSession, telegram_id: int, username: str | None, full_name: str | None
) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        changed = False
        if user.username != username:
            user.username = username
            changed = True
        if user.full_name != full_name:
            user.full_name = full_name
            changed = True
        if changed:
            await session.commit()
        return user

    # Первый человек, чей telegram_id совпадает с SUPER_ADMIN_ID из .env,
    # автоматически становится супер-админом при первом /start.
    role = "super_admin" if config.SUPER_ADMIN_ID and telegram_id == config.SUPER_ADMIN_ID else "user"
    user = User(telegram_id=telegram_id, username=username, full_name=full_name, role=role)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def set_user_language(session: AsyncSession, user: User, language: str) -> None:
    user.language = language
    await session.commit()


async def set_user_role(session: AsyncSession, telegram_id: int, role: str) -> bool:
    user = await get_user_by_telegram_id(session, telegram_id)
    if not user:
        return False
    user.role = role
    await session.commit()
    return True


async def is_admin(user: User) -> bool:
    return user.role in ("admin", "super_admin")


async def is_super_admin(user: User) -> bool:
    return user.role == "super_admin"


async def get_all_admins(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).where(User.role.in_(["admin", "super_admin"])))
    return list(result.scalars().all())


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------


async def ensure_default_prices(session: AsyncSession) -> None:
    """Заполняет таблицу цен стартовыми значениями при первом запуске."""
    result = await session.execute(select(Price))
    existing = {p.uc_amount for p in result.scalars().all()}
    order = len(existing)
    for amount, price in config.DEFAULT_UC_PRICES.items():
        if amount not in existing:
            order += 1
            session.add(Price(uc_amount=amount, price=price, sort_order=order))
    await session.commit()


async def get_active_prices(session: AsyncSession) -> list[Price]:
    result = await session.execute(
        select(Price).where(Price.is_active.is_(True)).order_by(Price.sort_order, Price.uc_amount)
    )
    return list(result.scalars().all())


async def get_all_prices(session: AsyncSession) -> list[Price]:
    result = await session.execute(select(Price).order_by(Price.sort_order, Price.uc_amount))
    return list(result.scalars().all())


async def get_price_by_amount(session: AsyncSession, uc_amount: int) -> Price | None:
    result = await session.execute(select(Price).where(Price.uc_amount == uc_amount))
    return result.scalar_one_or_none()


async def update_price(session: AsyncSession, uc_amount: int, new_price: int) -> bool:
    price = await get_price_by_amount(session, uc_amount)
    if not price:
        return False
    price.price = new_price
    price.is_active = True
    await session.commit()
    return True


async def add_price(session: AsyncSession, uc_amount: int, price_value: int) -> Price:
    existing = await get_price_by_amount(session, uc_amount)
    if existing:
        existing.price = price_value
        existing.is_active = True
        await session.commit()
        return existing

    result = await session.execute(select(Price))
    count = len(result.scalars().all())
    price = Price(uc_amount=uc_amount, price=price_value, sort_order=count + 1)
    session.add(price)
    await session.commit()
    await session.refresh(price)
    return price


async def deactivate_price(session: AsyncSession, uc_amount: int) -> bool:
    price = await get_price_by_amount(session, uc_amount)
    if not price:
        return False
    price.is_active = False
    await session.commit()
    return True


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------


async def create_order(
    session: AsyncSession, user: User, uc_amount: int, price: int, pubg_id: str, receipt_file_id: str
) -> Order:
    order = Order(
        user_id=user.id,
        uc_amount=uc_amount,
        price=price,
        pubg_id=pubg_id,
        receipt_file_id=receipt_file_id,
        status="pending",
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order(session: AsyncSession, order_id: int) -> Order | None:
    result = await session.execute(select(Order).options(selectinload(Order.user))
                                    .where(Order.id == order_id))
    return result.scalar_one_or_none()


async def get_pending_orders(session: AsyncSession) -> list[Order]:
    result = await session.execute(
        select(Order).options(selectinload(Order.user))
            .where(Order.status == "pending").order_by(Order.created_at)
    )
    return list(result.scalars().all())


async def get_user_orders(session: AsyncSession, user: User) -> list[Order]:
    result = await session.execute(
        select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc())
    )
    return list(result.scalars().all())


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    status: str,
    admin: User | None = None,
    comment: str | None = None,
) -> Order | None:
    order = await get_order(session, order_id)
    if not order:
        return None
    order.status = status
    if admin:
        order.admin_id = admin.id
    if comment:
        order.admin_comment = comment
    await session.commit()
    await session.refresh(order)
    return order


async def get_order_counts(session: AsyncSession, user: User) -> dict:
    orders = await get_user_orders(session, user)
    counts = {"approved": 0, "pending": 0, "rejected": 0, "cancelled": 0}
    for o in orders:
        if o.status in counts:
            counts[o.status] += 1
    return counts


# ---------------------------------------------------------------------------
# Action log (аудит каждого движения пользователя)
# ---------------------------------------------------------------------------


async def log_action(
    session: AsyncSession,
    telegram_id: int,
    action: str,
    details: str | None = None,
    user_id: int | None = None,
) -> None:
    log = ActionLog(user_id=user_id, telegram_id=telegram_id, action=action, details=details)
    session.add(log)
    await session.commit()
