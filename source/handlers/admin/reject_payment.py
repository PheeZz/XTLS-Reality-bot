from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db_manager
from source.keyboard import inline
from source.utils import localizer


async def reject_incoming_payment(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[-1]
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.reject_payment,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.admin_payment_notification_keyboard(
            language_code=call.from_user.language_code,
            from_user_id=user_id,
            is_payment_checked=True,
        ),
    )
    await call.bot.send_message(
        chat_id=user_id,
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.reject_payment,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.start_menu_kb(
            language_code=call.from_user.language_code, user_id=user_id
        ),
    )
