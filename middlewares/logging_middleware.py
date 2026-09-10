from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from database.requests import log_action
from utils.logger import logger


class ActionLoggingMiddleware(BaseMiddleware):
    """Пишет каждое действие пользователя (сообщение / нажатие кнопки)
    в таблицу action_logs и в файл bot.log — для аудита и отладки."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data.get("session")
        db_user = data.get("db_user")
        tg_user = data.get("event_from_user")

        if session is not None and tg_user is not None:
            if isinstance(event, Message):
                if event.photo:
                    action = "photo"
                    details = event.photo[-1].file_id
                else:
                    action = "message"
                    details = event.text or f"<{event.content_type}>"
            elif isinstance(event, CallbackQuery):
                action = "callback"
                details = event.data
            else:
                action = event.__class__.__name__
                details = None

            try:
                await log_action(
                    session,
                    tg_user.id,
                    action,
                    details,
                    user_id=db_user.id if db_user else None,
                )
            except Exception:
                logger.exception("Failed to write action log for user %s", tg_user.id)

            logger.info("user=%s (@%s) %s -> %s", tg_user.id, tg_user.username, action, details)

        return await handler(event, data)
