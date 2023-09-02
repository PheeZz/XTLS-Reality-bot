from aiogram import Dispatcher
from loguru import logger

from .accept_payment import *
from .reject_payment import *
from .show_user import *
from .delete_keyboard import *


def register_admin_handlers(dp: Dispatcher):
    try:
        dp.register_callback_query_handler(
            accept_incoming_payment,
            lambda call: call.data.startswith("accept_payment_"),
            state="*",
        )
        dp.register_callback_query_handler(
            reject_incoming_payment,
            lambda call: call.data.startswith("reject_payment_"),
            state="*",
        )
        dp.register_callback_query_handler(
            delete_keyboard,
            lambda call: call.data.startswith("delete_keyboard"),
            state="*",
        )
        dp.register_callback_query_handler(
            show_info_about_user_by_button,
            lambda call: call.data.startswith("show_user_"),
            state="*",
        )
    except Exception as e:
        logger.error(f"Error while registering admin handlers: {e}")
