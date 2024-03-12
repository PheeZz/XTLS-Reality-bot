from aiogram import Dispatcher
from loguru import logger

from .ban_toggle import *
from .give_bonus_configs import *
from .give_subscription import *
from .show_user_profile import *
from .show_users_configs import *


def register_admin_show_user_handlers(dp: Dispatcher):
    try:
        dp.register_callback_query_handler(
            show_info_about_user,
            lambda call: call.data.startswith("show_user")
            and not call.data.startswith("show_users_configs"),
            state="*",
        )
        dp.register_message_handler(
            check_is_user_exist,
            content_types=types.ContentTypes.TEXT,
            state=GetUserInfo.wait_for_user_id_or_username,
        )
        dp.register_callback_query_handler(
            switch_keyboard_to_user_configs,
            lambda call: call.data.startswith("show_users_configs_"),
            state="*",
        )
        dp.register_callback_query_handler(
            ask_admin_for_subscription_duration,
            lambda call: call.data.startswith("give_subscription_"),
            state="*",
        )
        dp.register_message_handler(
            check_is_duration_digit,
            content_types=types.ContentTypes.TEXT,
            state=GiveSubscription.wait_for_subscription_duration,
        )

        dp.register_callback_query_handler(
            toggle_ban_for_user,
            lambda call: call.data.startswith("ban_user_"),
            state="*",
        )

        dp.register_callback_query_handler(
            ask_admin_for_count_of_bonus_generations_to_give,
            lambda call: call.data.startswith("give_bonus_configs_"),
            state="*",
        )
        dp.register_message_handler(
            check_is_count_of_bonus_generations_to_give_digit,
            content_types=types.ContentTypes.TEXT,
            state=GiveBonusConfigGenerations.wait_for_bonus_config_generations_count,
        )

    except Exception as e:
        logger.error(f"Error while registering admin handlers: {e}")

    else:
        logger.info("Admin handlers for show user funcs registered successfully")
