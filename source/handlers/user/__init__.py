from aiogram import Dispatcher
from aiogram.types import ContentType
from loguru import logger

from source.utils.states.user import PaymentViaBankTransfer
from .start import *
from .pay import *
from .configs_menu.show_configs import *
from .my_profile import show_my_profile
from .ask_support import *

from .configs_menu import register_configs_menu_handlers


def register_user_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(start, commands="start", state="*")
        dp.register_callback_query_handler(
            main_menu_by_button,
            lambda call: call.data == "back_to_main_menu",
            state="*",
        )
        dp.register_message_handler(show_payment_method, commands="pay", state="*")

        dp.register_message_handler(
            notify_admin_about_new_payment,
            content_types=[
                ContentType.PHOTO,
                ContentType.DOCUMENT,
            ],
            state=PaymentViaBankTransfer.waiting_for_payment_screenshot_or_receipt,
        )

        dp.register_callback_query_handler(
            show_my_profile,
            lambda call: call.data == "my_profile",
            state="*",
        )

        dp.register_callback_query_handler(
            ask_user_for_question_to_support,
            lambda call: call.data == "create_support_ticket",
            state="*",
        )

        dp.register_message_handler(
            forward_question_to_admins,
            state=AskSupport.waiting_for_question,
        )

        register_configs_menu_handlers(dp)
    except Exception as e:
        logger.error(f"Error while registering user handlers: {e}")
    else:
        logger.info("User handlers registered successfully")
