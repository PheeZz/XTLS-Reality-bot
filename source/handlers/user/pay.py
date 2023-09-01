from loguru import logger
from source.data import config
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from source.utils.states.user import PaymentViaBankTransfer

from source.middlewares import rate_limit


@rate_limit(limit=1)
async def show_payment_method(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started payment")
    await state.finish()
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.payment_method_card,
        )
        .replace("{amount}", config.subscription_monthly_price)
        .replace("{payment_card}", config.payment_card),
        parse_mode=types.ParseMode.HTML,
    )
    await PaymentViaBankTransfer.waiting_for_payment_screenshot_or_receipt.set()


async def notify_admin_about_new_payment(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started payment")
    await state.finish()
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.payment_method_card_success,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    for admin_id in config.admins_ids:
        await message.forward(admin_id)
        await message.bot.send_message(
            chat_id=admin_id,
            text=localizer.get_user_localized_text(
                # FIXME: need to select admin language, instead of user language
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.admin_notification_about_new_payment,
            )
            .replace("{user_id}", str(message.from_user.id))
            .replace(
                "{username}",
                str(message.from_user.username)
                if message.from_user.username
                else str(message.from_user.full_name),
            ),
            parse_mode=types.ParseMode.HTML,
            reply_markup=await inline.admin_payment_notification_keyboard(
                # FIXME: need to select admin language, instead of user language
                language_code=message.from_user.language_code,
                from_user_id=message.from_user.id,
            ),
        )
