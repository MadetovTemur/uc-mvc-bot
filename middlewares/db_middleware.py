from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database.db import async_session
from database.requests import get_or_create_user


class DbSessionMiddleware(BaseMiddleware):
    """Открывает сессию БД на каждое обновление и подгружает / создаёт
    пользователя, кладёт их в data как session / db_user / lang, чтобы
    любой хендлер и фильтр мог их получить как обычные аргументы."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with async_session() as session:
            data["session"] = session

            tg_user = data.get("event_from_user")
            if tg_user is not None:
                user = await get_or_create_user(
                    session, tg_user.id, tg_user.username, tg_user.full_name
                )
                data["db_user"] = user
                data["lang"] = user.language

            return await handler(event, data)
