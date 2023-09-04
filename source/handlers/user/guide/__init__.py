from aiogram import Dispatcher
from aiogram.types import ContentType
from loguru import logger

from .guide_menu import show_help_guide
from .android import show_help_guide_android
from .ios import show_help_guide_ios
from .pc import show_help_guide_pc


def register_show_help_guide_handlers(dp: Dispatcher):
    try:
        dp.register_message_handler(
            show_help_guide,
            commands=["help", "guide", "h"],
            state="*",
        )
        dp.register_callback_query_handler(
            show_help_guide_ios,
            lambda call: call.data == "show_help_ios",
            state="*",
        )
        dp.register_callback_query_handler(
            show_help_guide_android,
            lambda call: call.data == "show_help_android",
            state="*",
        )
        dp.register_callback_query_handler(
            show_help_guide_pc,
            lambda call: call.data == "show_help_pc",
            state="*",
        )

    except Exception as err:
        logger.error(f"Error while registering show_help_guide handlers: {err}")

    else:
        logger.info("show_help_guide handlers registered successfully")
