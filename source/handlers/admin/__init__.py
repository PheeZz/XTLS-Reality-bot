from aiogram import Dispatcher, types
from loguru import logger

from source.utils.callback import support_callback

from .accept_payment import *
from .answer_support import *
from .create_mailing import (
    CreateMailing,
    confirm_mailing_message,
    create_mailing_message,
    send_mailing_message,
)
from .delete_keyboard import *
from .reject_payment import *
from .show_stats import *
from .show_user import register_admin_show_user_handlers


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
            ask_admin_for_support_answer,
            # allow any callback data with support_callback
            support_callback.filter(),
            state="*",
        )

        dp.register_message_handler(
            send_support_answer_to_user,
            state=AnswerSupport.wait_for_support_answer,
        )

        dp.register_callback_query_handler(
            show_global_stats,
            lambda call: call.data.startswith("show_statistics"),
            state="*",
        )

        dp.register_callback_query_handler(
            create_mailing_message,
            lambda call: call.data.startswith("create_mailing"),
            state="*",
        )

        dp.register_message_handler(
            confirm_mailing_message,
            state=CreateMailing.wait_for_mailing_message,
            content_types=[
                types.ContentType.TEXT,
                types.ContentType.PHOTO,
                types.ContentType.VIDEO,
            ],
        )
        dp.register_callback_query_handler(
            send_mailing_message,
            lambda call: call.data.startswith("confirm_mailing_message"),
            state=CreateMailing.wait_for_confirmation,
        )

        register_admin_show_user_handlers(dp)

    except Exception as e:
        logger.error(f"Error while registering admin handlers: {e}")

    else:
        logger.info("Admin handlers registered successfully")
