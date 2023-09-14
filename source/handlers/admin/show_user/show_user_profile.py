from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from source.utils.states.admin import GetUserInfo
from source.utils import localizer

from loader import db_manager, bot


async def show_info_about_user(
    call_or_message: types.CallbackQuery | types.Message,
    state: FSMContext,
    user_id: int | None = None,
):
    user_id = call_or_message.data.split("_")[-1] if not user_id else user_id
    if isinstance(user_id, str) and not user_id.isdigit():
        await request_user_id_or_username(call=call_or_message, state=state)
        return

    if isinstance(call_or_message, types.CallbackQuery):
        message = call_or_message.message
    else:
        message = call_or_message

    await message.answer(
        text=await create_user_info_message_text(user_id=user_id),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.admin_user_info_keyboard(
            language_code=call_or_message.from_user.language_code,
            user_id=user_id,
        ),
    )


async def create_user_info_message_text(user_id: int) -> str:
    db_user_info = await db_manager.get_user_by_id(user_id=user_id)
    subscription_days_left = (
        db_user_info.subscription_end_date - datetime.now().date()
    ).days
    if subscription_days_left < 0:
        subscription_days_left = 0

    language_code = (
        await bot.get_chat_member(chat_id=user_id, user_id=user_id)
    ).user.language_code
    text = localizer.get_user_localized_text(
        user_language_code=language_code,
        text_localization=localizer.message.user_info,
    ).format(
        user_id=user_id,
        user_username=db_user_info.username,
        is_not_banned=db_user_info.is_not_banned,
        is_active_subscription=db_user_info.is_active_subscription,
        subscription_end_date=db_user_info.subscription_end_date.strftime("%d.%m.%Y"),
        subscription_days_left=subscription_days_left,
        configs_count=db_user_info.configs_count,
        bonus_configs_count=db_user_info.bonus_configs_count,
        unused_configs_count=db_user_info.unused_configs_count,
        created_at=db_user_info.created_at.strftime("%d.%m.%Y %H:%M:%S"),
    )
    return text


async def request_user_id_or_username(call: types.CallbackQuery, state: FSMContext):
    await GetUserInfo.wait_for_user_id_or_username.set()

    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.request_user_id_or_username,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code
        ),
        parse_mode=types.ParseMode.HTML,
    )


async def check_is_user_exist(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        username = message.text.replace("@", "")
        user_id = await db_manager.get_user_id_by_username(username=username)
        is_user_exist = user_id != None

    else:
        user_id = int(message.text)
        is_user_exist = await db_manager.is_user_registered(user_id=user_id)

    if not is_user_exist:
        await message.answer(
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.error_user_not_found,
            ),
            parse_mode=types.ParseMode.HTML,
        )
        return

    await state.finish()
    await show_info_about_user(call_or_message=message, state=state, user_id=user_id)
