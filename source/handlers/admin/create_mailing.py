from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from source.utils import Mailer, localizer
from source.utils.states.admin import CreateMailing


async def create_mailing_message(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.create_mailing_message,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
    await CreateMailing.wait_for_mailing_message.set()


async def confirm_mailing_message(message: types.Message, state: FSMContext):
    await state.update_data(mailing_message=message)
    await CreateMailing.wait_for_confirmation.set()
    await Mailer(message=message).echo()

    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.confirm_mailing_message,
        ),
        reply_markup=await inline.insert_button_confirm_mailing_message(
            language_code=message.from_user.language_code,
        ),
    )


async def send_mailing_message(call: types.CallbackQuery, state: FSMContext):
    mailing_message: types.Message = (await state.get_data()).get("mailing_message")
    await Mailer(message=mailing_message).run_mailing_post()
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.mailing_message_sent,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
    await state.finish()
