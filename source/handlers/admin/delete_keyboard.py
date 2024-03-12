from aiogram import types
from aiogram.dispatcher import FSMContext

from source.utils import localizer


async def delete_keyboard(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
