from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from source.utils.states.admin import GiveBonusConfigGenerations
from source.utils import localizer
from source.utils.etc import is_text_int_number
from ..show_user.show_user_profile import show_info_about_user
from loader import db_manager

from loguru import logger


async def ask_admin_for_count_of_bonus_generations_to_give(
    call: types.CallbackQuery, state: FSMContext
):
    user_id = call.data.split("_")[-1]
    await state.update_data(user_id=user_id)
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.ask_admin_for_count_of_bonus_generations_to_give,
        ),
    )
    await GiveBonusConfigGenerations.wait_for_bonus_config_generations_count.set()


async def check_is_count_of_bonus_generations_to_give_digit(
    message: types.Message, state: FSMContext
):
    if not is_text_int_number(message.text):
        await message.answer(
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.count_of_bonus_generations_to_give_must_be_digit,
            ),
        )
        return
    await state.update_data(bonus_config_generations_count=int(message.text))
    await give_bonus_config_generations_to_user_and_notify_him(
        message=message, state=state
    )


async def give_bonus_config_generations_to_user_and_notify_him(
    message: types.Message, state: FSMContext
):
    data = await state.get_data()
    user_id: int = data.get("user_id")
    bonus_config_generations_count: int = data.get("bonus_config_generations_count")
    await db_manager.upsert_bonus_config_generations_to_user(
        user_id=user_id, new_bonus_config_count=bonus_config_generations_count
    )
    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.admin_give_you_bonus_config_generations,
            ).format(
                count=bonus_config_generations_count,
            ),
            parse_mode=types.ParseMode.HTML
        )
    except BotBlocked:
        logger.error(f"Bot blocked by user {user_id}")
    await show_info_about_user(call_or_message=message, state=state, user_id=user_id)
