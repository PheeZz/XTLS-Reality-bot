from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from source.keyboard import inline
from source.utils.states.admin import GiveSubscription
from source.utils import localizer
from ..show_user.show_user_profile import show_info_about_user
from loader import db_manager

from loguru import logger


async def ask_admin_for_subscription_duration(
    call: types.CallbackQuery, state: FSMContext
):
    user_id = call.data.split("_")[-1]
    await state.update_data(user_id=user_id)
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.ask_admin_for_subscription_duration,
        ),
    )
    await GiveSubscription.wait_for_subscription_duration.set()


async def check_is_duration_digit(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.subscription_duration_must_be_digit,
            ),
        )
        return
    await state.update_data(subscription_duration=int(message.text))
    await give_subscription_to_user_and_notify_him(message=message, state=state)


async def give_subscription_to_user_and_notify_him(
    message: types.Message, state: FSMContext
):
    data = await state.get_data()
    user_id: int = data.get("user_id")
    subscription_duration: int = data.get("subscription_duration")
    await db_manager.add_days_to_user_subscription(
        user_id=user_id, days=subscription_duration
    )
    try:
        await message.bot.send_message(
            chat_id=user_id,
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.admin_give_you_days_subscription,
            ).format(
                days=subscription_duration,
            ),
            parse_mode=types.ParseMode.HTML
        )
    except BotBlocked:
        logger.error(f"Bot blocked by user {user_id}")

    finally:
        await show_info_about_user(
            call_or_message=message, state=state, user_id=user_id
        )
        await state.finish()
