from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from source.handlers.admin.show_user.show_user_profile import (
    create_user_info_message_text,
)
from source.keyboard import inline
from source.middlewares import rate_limit

from .check_is_user_banned import is_user_banned


@rate_limit(limit=1)
@is_user_banned
async def show_my_profile(
    call: types.CallbackQuery,
    state: FSMContext,
):
    logger.info(f"User {call.from_user.id} requested info about himself")
    await call.message.answer(
        text=await create_user_info_message_text(user_id=call.from_user.id),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
