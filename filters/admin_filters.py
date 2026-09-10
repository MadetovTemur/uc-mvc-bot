from aiogram.filters import BaseFilter

from database.models import User


class IsAdmin(BaseFilter):
    async def __call__(self, event, db_user: User | None = None) -> bool:
        return bool(db_user) and db_user.role in ("admin", "super_admin")


class IsSuperAdmin(BaseFilter):
    async def __call__(self, event, db_user: User | None = None) -> bool:
        return bool(db_user) and db_user.role == "super_admin"
