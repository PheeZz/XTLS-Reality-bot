from aiogram import Dispatcher
from aiogram.types import ContentType
from loguru import logger

from .show_configs import *
from .create_new_config import *
from .show_specified_config import *


def register_configs_menu_handlers(dp: Dispatcher):
    try:
        dp.register_callback_query_handler(
            show_user_configs,
            lambda call: call.data.startswith("my_configs"),
            state="*",
        )

        dp.register_callback_query_handler(
            request_user_for_config_name,
            lambda call: call.data.startswith("create_new_config"),
            state="*",
        )

        dp.register_message_handler(
            generate_config_for_user,
            content_types=ContentType.TEXT,
            state=GeneratingNewConfig.waiting_for_config_name,
        )

        dp.register_callback_query_handler(
            show_specified_config,
            lambda call: call.data.startswith("show_config_"),
            state="*",
        )
    except Exception as e:
        logger.error(f"Error while registering configs_menu handlers: {e}")
    else:
        logger.info("Configs_menu handlers registered successfully")
