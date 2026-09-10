import re

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import config
from database.models import User
from database.requests import (
    create_order,
    get_active_prices,
    get_all_admins,
    get_order_counts,
    get_price_by_amount,
    get_user_orders,
)
from keyboards.user_kb import uc_amounts_kb
from locales.translations import t
from states.states import BuyUC
from utils.logger import logger

router = Router(name="user")

PUBG_ID_RE = re.compile(r"^\d{5,15}$")


def fmt_money(value: int) -> str:
    return f"{value:,}".replace(",", " ")


@router.message(F.text.in_(["💹 UC narxlari", "💹 Цены на UC"]))
async def show_prices(message: Message, session, lang: str, state: FSMContext):
    await state.clear()
    prices = await get_active_prices(session)
    text = t(lang, "prices_title")
    for p in prices:
        text += t(lang, "price_line", amount=p.uc_amount, price=fmt_money(p.price))
    await message.answer(text)


@router.message(F.text.in_(["♻️ UC xarid qilish", "♻️ Купить UC"]))
async def start_buy(message: Message, session, lang: str, state: FSMContext):
    prices = await get_active_prices(session)
    amounts = [p.uc_amount for p in prices]
    await state.set_state(BuyUC.choosing_amount)
    await message.answer(
        t(lang, "choose_uc_amount") + t(lang, "cancel_hint"),
        reply_markup=uc_amounts_kb(amounts),
    )


@router.message(BuyUC.choosing_amount)
async def choose_amount(message: Message, session, lang: str, state: FSMContext):
    match = re.match(r"^(\d+)\s*UC$", (message.text or "").strip(), re.IGNORECASE)
    if not match:
        await message.answer(t(lang, "invalid_number"))
        return

    amount = int(match.group(1))
    price = await get_price_by_amount(session, amount)
    if not price or not price.is_active:
        await message.answer(t(lang, "invalid_number"))
        return

    await state.update_data(uc_amount=amount, price=price.price)
    await state.set_state(BuyUC.entering_pubg_id)
    await message.answer(t(lang, "enter_pubg_id") + t(lang, "cancel_hint"))


@router.message(BuyUC.entering_pubg_id)
async def enter_pubg_id(message: Message, lang: str, state: FSMContext):
    pubg_id = (message.text or "").strip()
    if not PUBG_ID_RE.match(pubg_id):
        await message.answer(t(lang, "invalid_pubg_id"))
        return

    await state.update_data(pubg_id=pubg_id)
    data = await state.get_data()
    await state.set_state(BuyUC.sending_receipt)
    await message.answer(
        t(
            lang,
            "confirm_order",
            amount=data["uc_amount"],
            price=fmt_money(data["price"]),
            pubg_id=pubg_id,
        )
    )
    await message.answer(t(lang, "send_receipt") + t(lang, "cancel_hint"))


@router.message(BuyUC.sending_receipt, F.photo)
async def receive_receipt(message: Message, session, db_user: User, lang: str, state: FSMContext):
    from handlers.common import menu_for  # локальный импорт, чтобы избежать циклического импорта

    data = await state.get_data()
    receipt_file_id = message.photo[-1].file_id

    order = await create_order(
        session, db_user, data["uc_amount"], data["price"], data["pubg_id"], receipt_file_id
    )
    await state.clear()

    await message.answer(
        t(lang, "order_created", order_id=order.id),
        reply_markup=await menu_for(db_user, lang),
    )

    await notify_admins_new_order(message.bot, session, order, db_user)


@router.message(BuyUC.sending_receipt)
async def receipt_not_photo(message: Message, lang: str):
    await message.answer(t(lang, "not_a_photo"))


async def notify_admins_new_order(bot, session, order, user: User):
    from keyboards.admin_kb import order_action_kb  # локальный импорт против циклического импорта

    admins = await get_all_admins(session)
    for admin in admins:
        text = t(
            admin.language,
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
        try:
            await bot.send_photo(
                admin.telegram_id,
                order.receipt_file_id,
                caption=text,
                reply_markup=order_action_kb(order.id, admin.language),
            )
        except Exception:
            logger.exception("Failed to notify admin %s about new order", admin.telegram_id)


@router.message(F.text.in_(["🧮 Orderlar ro'yxati", "🧮 Список заказов"]))
async def show_orders(message: Message, session, db_user: User, lang: str, state: FSMContext):
    await state.clear()
    orders = await get_user_orders(session, db_user)
    if not orders:
        await message.answer(t(lang, "orders_empty"))
        return

    counts = await get_order_counts(session, db_user)
    text = t(
        lang,
        "orders_stats",
        approved=counts["approved"],
        pending=counts["pending"],
        rejected_cancelled=counts["rejected"] + counts["cancelled"],
    )
    text += "\n\n"

    status_key = {
        "pending": "order_status_pending",
        "approved": "order_status_approved",
        "rejected": "order_status_rejected",
        "cancelled": "order_status_cancelled",
    }
    for o in orders[:20]:
        text += (
            t(
                lang,
                "order_item",
                id=o.id,
                amount=o.uc_amount,
                price=fmt_money(o.price),
                status=t(lang, status_key[o.status]),
            )
            + "\n"
        )
    await message.answer(text)


@router.message(F.text.in_(["👥 Biz xaqimizda", "👥 О нас"]))
async def about_us(message: Message, lang: str, state: FSMContext):
    await state.clear()
    await message.answer(t(lang, "about_us", contact=config.SUPPORT_CONTACT))
