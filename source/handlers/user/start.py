from loguru import logger
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline


async def start(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started bot")
    await state.finish()
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
