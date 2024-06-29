import os
from aiogram import types
from aiogram.filters import BaseFilter


class AdminFilter(BaseFilter):
    async def __call__(self, message: types.Message):
        user = message.from_user
        return user.id == int(os.environ.get("ADMIN_CHAT_ID"))
