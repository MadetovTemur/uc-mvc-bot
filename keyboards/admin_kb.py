from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from locales.translations import t


def admin_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "admin_pending_orders"))
    b.button(text=t(lang, "admin_manage_prices"))
    b.button(text=t(lang, "admin_manage_admins"))
    b.button(text=t(lang, "admin_stats"))
    b.button(text=t(lang, "menu_language"))
    b.adjust(1, 1, 1, 1, 1)
    return b.as_markup(resize_keyboard=True)


def order_action_kb(order_id: int, lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "approve"), callback_data=f"order:approve:{order_id}")
    b.button(text=t(lang, "reject"), callback_data=f"order:reject:{order_id}")
    b.adjust(2)
    return b.as_markup()


def price_list_kb(prices, lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for p in prices:
        mark = "" if p.is_active else " 🚫"
        b.button(text=f"{p.uc_amount} UC — {p.price}{mark}", callback_data=f"editprice:{p.uc_amount}")
    b.button(text=t(lang, "add_new_uc"), callback_data="addprice:new")
    b.adjust(2)
    return b.as_markup()


def admin_manage_kb(lang: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text=t(lang, "add_admin_prompt"), callback_data="admin:add")
    b.button(text=t(lang, "remove_admin_prompt"), callback_data="admin:remove")
    b.adjust(1)
    return b.as_markup()
