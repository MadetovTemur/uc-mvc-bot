from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from locales.translations import t


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    b.button(text=t(lang, "menu_prices"))
    b.button(text=t(lang, "menu_buy"))
    b.button(text=t(lang, "menu_orders"))
    b.button(text=t(lang, "menu_about"))
    b.button(text=t(lang, "menu_language"))
    b.adjust(1, 1, 2, 1)
    return b.as_markup(resize_keyboard=True)


def language_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🇺🇿 O'zbekcha", callback_data="lang:uz")
    b.button(text="🇷🇺 Русский", callback_data="lang:ru")
    b.adjust(2)
    return b.as_markup()


def uc_amounts_kb(amounts: list[int]) -> ReplyKeyboardMarkup:
    b = ReplyKeyboardBuilder()
    for amount in amounts:
        b.button(text=f"{amount} UC")
    b.adjust(3)
    return b.as_markup(resize_keyboard=True)
