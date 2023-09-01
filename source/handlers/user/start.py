from loguru import logger
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from loader import db_manager


async def start(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started bot")
    await state.finish()
    await db_manager.upsert_new_user(
        user_id=message.from_user.id,
        username=message.from_user.username if message.from_user.username else None,
    )
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.new_user_greeting,
        ).replace("{user}", message.from_user.full_name),
        reply_markup=await inline.start_menu_kb(
            language_code=message.from_user.language_code, user_id=message.from_user.id
        ),
        parse_mode=types.ParseMode.HTML,
    )
