from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext


async def delete_keyboard(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
