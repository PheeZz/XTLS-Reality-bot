from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from ..show_user.show_user_profile import show_info_about_user
from loader import db_manager


async def toggle_ban_for_user(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[-1]
    await db_manager.toggle_user_banned_status(user_id=user_id)
    await show_info_about_user(call_or_message=call, state=state)
