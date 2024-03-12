from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db_manager
from source.keyboard import inline
from source.utils import localizer


async def accept_incoming_payment(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[-1]
    if await db_manager.add_days_to_user_subscription(user_id=user_id, days=30):
        await notify_about_success(call=call, user_id=user_id)
    else:
        await notify_about_error(call=call, user_id=user_id)


async def notify_about_success(call: types.CallbackQuery, user_id: int):
    # edit message for admin
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.payment_accepted_for_admin,
        ).replace("{days}", "30"),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.admin_payment_notification_keyboard(
            language_code=call.from_user.language_code,
            from_user_id=user_id,
            is_payment_checked=True,
        ),
    )
    # send message for user
    await call.bot.send_message(
        chat_id=user_id,
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.payment_accepted_for_user,
        ).replace("{days}", "30"),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.start_menu_kb(
            language_code=call.from_user.language_code, user_id=user_id
        ),
    )


async def notify_about_error(call: types.CallbackQuery, user_id: int):
    # edit message for admin
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.error_while_accepting_payment,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.admin_payment_notification_keyboard(
            language_code=call.from_user.language_code,
            from_user_id=user_id,
            is_payment_checked=True,
        ),
    )
    # send message for user
    await call.bot.send_message(
        chat_id=user_id,
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.error_while_accepting_payment,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.start_menu_kb(
            language_code=call.from_user.language_code, user_id=user_id
        ),
    )
