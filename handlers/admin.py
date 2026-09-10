from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import func, select

from database.models import Order, User
from database.requests import (
    add_price,
    get_all_prices,
    get_order,
    get_pending_orders,
    get_price_by_amount,
    get_user_by_telegram_id,
    set_user_role,
    update_order_status,
    update_price,
)
from filters.admin_filters import IsAdmin, IsSuperAdmin
from keyboards.admin_kb import admin_manage_kb, order_action_kb, price_list_kb
from locales.translations import t
from states.states import AdminManage, AdminPrice, AdminReject
from utils.logger import logger

router = Router(name="admin")
# Все хендлеры в этом роутере доступны только admin / super_admin.
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


def fmt_money(value: int) -> str:
    return f"{value:,}".replace(",", " ")


# ---------------------------------------------------------------------------
# Заказы: список ожидающих + подтверждение / отклонение
# ---------------------------------------------------------------------------


@router.message(F.text.in_(["📥 Kutilayotgan buyurtmalar", "📥 Ожидающие заказы"]))
async def list_pending(message: Message, session, lang: str, state: FSMContext):
    await state.clear()
    orders = await get_pending_orders(session)
    if not orders:
        await message.answer(t(lang, "admin_no_pending"))
        return
    
    for order in orders:
        user = order.user
        text = t(
            lang,
            "admin_order_card",
            id=order.id,
            full_name=user.full_name,
            username=user.username or "-",
            telegram_id=user.telegram_id,
            pubg_id=order.pubg_id,
            amount=order.uc_amount,
            price=fmt_money(order.price),
            created_at=order.created_at.strftime("%d.%m.%Y %H:%M"),
        )
        await message.answer_photo(
            order.receipt_file_id, caption=text, reply_markup=order_action_kb(order.id, lang)
        )


@router.callback_query(F.data.startswith("order:approve:"))
async def approve_order(callback: CallbackQuery, session, db_user: User, lang: str):
    order_id = int(callback.data.split(":")[2])
    order = await get_order(session, order_id)
    if not order or order.status != "pending":
        await callback.answer(t(lang, "admin_no_pending"), show_alert=True)
        return

    order = await update_order_status(session, order_id, "approved", admin=db_user)
    user = order.user

    try:
        await callback.message.edit_caption(caption=(callback.message.caption or "") + "\n\n✅")
    except Exception:
        pass
    await callback.answer(t(lang, "order_approved_admin", id=order.id))

    try:
        await callback.bot.send_message(
            user.telegram_id,
            t(
                user.language,
                "order_approved_notify",
                order_id=order.id,
                amount=order.uc_amount,
                pubg_id=order.pubg_id,
            ),
        )
    except Exception:
        logger.exception("Failed to notify user %s about approval", user.telegram_id)


@router.callback_query(F.data.startswith("order:reject:"))
async def reject_order_start(callback: CallbackQuery, lang: str, state: FSMContext):
    order_id = int(callback.data.split(":")[2])
    await state.update_data(reject_order_id=order_id)
    await state.set_state(AdminReject.entering_reason)
    await callback.message.answer(t(lang, "enter_reject_reason"))
    await callback.answer()


@router.message(AdminReject.entering_reason)
async def reject_order_finish(message: Message, session, db_user: User, lang: str, state: FSMContext):
    data = await state.get_data()
    order_id = data.get("reject_order_id")
    reason = (message.text or "").strip()
    await state.clear()

    if not order_id:
        return

    order = await update_order_status(session, order_id, "rejected", admin=db_user, comment=reason)
    if not order:
        return

    user = order.user
    await message.answer(t(lang, "order_rejected_admin", id=order.id))

    try:
        await message.bot.send_message(
            user.telegram_id,
            t(user.language, "order_rejected_notify", order_id=order.id, reason=reason),
        )
    except Exception:
        logger.exception("Failed to notify user %s about rejection", user.telegram_id)


# ---------------------------------------------------------------------------
# Цены
# ---------------------------------------------------------------------------


@router.message(F.text.in_(["💰 Narxlarni boshqarish", "💰 Управление ценами"]))
async def manage_prices(message: Message, session, lang: str, state: FSMContext):
    await state.clear()
    prices = await get_all_prices(session)
    await message.answer(t(lang, "choose_price_to_edit"), reply_markup=price_list_kb(prices, lang))


@router.callback_query(F.data.startswith("editprice:"))
async def edit_price_start(callback: CallbackQuery, lang: str, state: FSMContext):
    amount = int(callback.data.split(":")[1])
    await state.update_data(edit_amount=amount)
    await state.set_state(AdminPrice.entering_new_price)
    await callback.message.answer(t(lang, "enter_new_price", amount=amount))
    await callback.answer()


@router.message(AdminPrice.entering_new_price)
async def edit_price_finish(message: Message, session, lang: str, state: FSMContext):
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(t(lang, "invalid_number"))
        return

    data = await state.get_data()
    amount = data["edit_amount"]
    new_price = int(raw)
    await update_price(session, amount, new_price)
    await state.clear()
    await message.answer(t(lang, "price_updated", amount=amount, price=fmt_money(new_price)))


@router.callback_query(F.data == "addprice:new")
async def add_price_start(callback: CallbackQuery, lang: str, state: FSMContext):
    await state.set_state(AdminPrice.entering_new_amount)
    await callback.message.answer(t(lang, "enter_new_uc_amount"))
    await callback.answer()


@router.message(AdminPrice.entering_new_amount)
async def add_price_amount(message: Message, session, lang: str, state: FSMContext):
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(t(lang, "invalid_number"))
        return

    amount = int(raw)
    existing = await get_price_by_amount(session, amount)
    await state.update_data(new_amount=amount)
    await state.set_state(AdminPrice.entering_new_amount_price)
    prompt_key = "enter_new_price" if existing else "enter_new_uc_price"
    await message.answer(t(lang, prompt_key, amount=amount))


@router.message(AdminPrice.entering_new_amount_price)
async def add_price_value(message: Message, session, lang: str, state: FSMContext):
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(t(lang, "invalid_number"))
        return

    data = await state.get_data()
    amount = data["new_amount"]
    price_value = int(raw)
    await add_price(session, amount, price_value)
    await state.clear()
    await message.answer(t(lang, "price_updated", amount=amount, price=fmt_money(price_value)))


# ---------------------------------------------------------------------------
# Управление админами (только супер-админ)
# ---------------------------------------------------------------------------


@router.message(F.text.in_(["👤 Adminlarni boshqarish", "👤 Управление админами"]), IsSuperAdmin())
async def manage_admins(message: Message, lang: str, state: FSMContext):
    await state.clear()
    await message.answer(t(lang, "admin_panel"), reply_markup=admin_manage_kb(lang))


@router.callback_query(F.data == "admin:add", IsSuperAdmin())
async def add_admin_start(callback: CallbackQuery, lang: str, state: FSMContext):
    await state.set_state(AdminManage.adding_admin_id)
    await callback.message.answer(t(lang, "add_admin_prompt") + t(lang, "cancel_hint"))
    await callback.answer()


@router.message(AdminManage.adding_admin_id, IsSuperAdmin())
async def add_admin_finish(message: Message, session, lang: str, state: FSMContext):
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(t(lang, "invalid_number"))
        return

    telegram_id = int(raw)
    target = await get_user_by_telegram_id(session, telegram_id)
    await state.clear()
    if not target:
        await message.answer(t(lang, "user_not_found"))
        return

    await set_user_role(session, telegram_id, "admin")
    await message.answer(t(lang, "admin_added"))


@router.callback_query(F.data == "admin:remove", IsSuperAdmin())
async def remove_admin_start(callback: CallbackQuery, lang: str, state: FSMContext):
    await state.set_state(AdminManage.removing_admin_id)
    await callback.message.answer(t(lang, "remove_admin_prompt") + t(lang, "cancel_hint"))
    await callback.answer()


@router.message(AdminManage.removing_admin_id, IsSuperAdmin())
async def remove_admin_finish(message: Message, session, lang: str, state: FSMContext):
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer(t(lang, "invalid_number"))
        return

    telegram_id = int(raw)
    target = await get_user_by_telegram_id(session, telegram_id)
    await state.clear()
    if not target:
        await message.answer(t(lang, "user_not_found"))
        return

    await set_user_role(session, telegram_id, "user")
    await message.answer(t(lang, "admin_removed"))


# ---------------------------------------------------------------------------
# Статистика
# ---------------------------------------------------------------------------


@router.message(F.text.in_(["📈 Statistika", "📈 Статистика"]))
async def show_stats(message: Message, session, lang: str, state: FSMContext):
    await state.clear()
    users_count = (await session.execute(select(func.count(User.id)))).scalar_one()
    orders_count = (await session.execute(select(func.count(Order.id)))).scalar_one()
    pending = (
        await session.execute(select(func.count(Order.id)).where(Order.status == "pending"))
    ).scalar_one()
    approved = (
        await session.execute(select(func.count(Order.id)).where(Order.status == "approved"))
    ).scalar_one()
    rejected = (
        await session.execute(select(func.count(Order.id)).where(Order.status == "rejected"))
    ).scalar_one()

    await message.answer(
        t(
            lang,
            "stats_text",
            users=users_count,
            orders=orders_count,
            pending=pending,
            approved=approved,
            rejected=rejected,
        )
    )
