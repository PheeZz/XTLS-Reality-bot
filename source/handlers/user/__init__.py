from loader import dp
from aiogram import Dispatcher
from aiogram.types import ContentType
from loguru import logger

from source.utils.states.user import PaymentViaBankTransfer
from .start import *
from .pay import *


def register_user_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(start, commands="start", state="*")

        dp.register_message_handler(show_payment_method, commands="pay", state="*")

        dp.register_message_handler(
            notify_admin_about_new_payment,
            content_types=[
                ContentType.PHOTO,
                ContentType.DOCUMENT,
            ],
            state=PaymentViaBankTransfer.waiting_for_payment_screenshot_or_receipt,
        )

    except Exception as e:
        logger.error(f"Error while registering user handlers: {e}")
