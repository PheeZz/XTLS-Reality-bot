from aiogram import types
from aiogram.dispatcher import FSMContext
from loguru import logger

from loader import db_manager
from source.data import config
from source.keyboard import inline
from source.utils import localizer


def is_user_banned(func):
    async def wrapper(message_or_call: types.Message | types.CallbackQuery, state: FSMContext):
        user_id = message_or_call.from_user.id
        if user_id not in config.admins_ids:
            if isinstance(message_or_call, types.CallbackQuery):
                message = message_or_call.message
                language_code = (
                    await message_or_call.bot.get_chat_member(chat_id=user_id, user_id=user_id)
                ).user.language_code
            else:
                message = message_or_call
                language_code = message_or_call.from_user.language_code

            if await db_manager.check_is_user_banned(user_id=user_id):
                await message.answer(
                    text=localizer.get_user_localized_text(
                        user_language_code=language_code,
                        text_localization=localizer.message.you_are_banned,
                    ),
                    reply_markup=await inline.insert_button_support(
                        language_code=language_code,
                    ),
                )
                await state.finish()
                return
        await func(message_or_call, state)

    return wrapper
