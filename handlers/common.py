from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models import User
from database.requests import is_admin, set_user_language
from keyboards.admin_kb import admin_menu_kb
from keyboards.user_kb import language_kb, main_menu_kb
from locales.translations import t

router = Router(name="common")


async def menu_for(user: User, lang: str):
    return admin_menu_kb(lang) if await is_admin(user) else main_menu_kb(lang)


@router.message(CommandStart())
async def cmd_start(message: Message, db_user: User, lang: str, state: FSMContext):
    await state.clear()
    await message.answer(
        t(lang, "welcome", name=message.from_user.full_name),
        reply_markup=await menu_for(db_user, lang),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, db_user: User, lang: str, state: FSMContext):
    current = await state.get_state()
    if current is None:
        await message.answer(t(lang, "nothing_to_cancel"))
        return
    await state.clear()
    await message.answer(t(lang, "cancelled"), reply_markup=await menu_for(db_user, lang))


@router.message(F.text == "🌐 Til / Язык")
async def choose_language(message: Message, lang: str, state: FSMContext):
    await state.clear()
    await message.answer(t(lang, "choose_language"), reply_markup=language_kb())


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, session, db_user: User):
    new_lang = callback.data.split(":")[1]
    if new_lang not in ("uz", "ru"):
        await callback.answer()
        return
    await set_user_language(session, db_user, new_lang)
    await callback.message.answer(
        t(new_lang, "language_set"), reply_markup=await menu_for(db_user, new_lang)
    )
    await callback.answer()
