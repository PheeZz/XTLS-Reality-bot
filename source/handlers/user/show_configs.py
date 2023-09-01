from loguru import logger
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline


async def show_user_configs(call: types.CallbackQuery, state: FSMContext):
    ...
