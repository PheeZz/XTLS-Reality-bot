from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from source.data import config
from source.utils import localizer
from source.utils.callback import support_callback
from loader import db_manager


async def insert_button_support(
    keyboard: InlineKeyboardMarkup | None = None, language_code: str = "ru"
):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.support,
            ),
            callback_data="create_support_ticket",
        )
    )
    return keyboard


async def start_menu_kb(language_code: str, user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.my_configs,
            ),
            callback_data="my_configs",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.my_profile,
            ),
            callback_data="my_profile",
        ),
    ]

    for button in buttons:
        keyboard.insert(button)

    keyboard = await insert_button_support(
        keyboard=keyboard, language_code=language_code
    )

    if user_id in config.admins_ids:
        keyboard = await add_buttons_for_admin_main_menu(
            keyboard=keyboard, language_code=language_code
        )

    return keyboard


async def add_buttons_for_admin_main_menu(
    keyboard: InlineKeyboardMarkup, language_code: str
):
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.show_user,
            ),
            callback_data="show_user",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.show_statistics,
            ),
            callback_data="show_statistics",
        ),
    ]
    for button in buttons:
        keyboard.insert(button)
    return keyboard


async def admin_payment_notification_keyboard(
    language_code: str, from_user_id: int, is_payment_checked: bool = False
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if not is_payment_checked:
        buttons = [
            InlineKeyboardButton(
                text=localizer.get_user_localized_text(
                    user_language_code=language_code,
                    text_localization=localizer.button.accept,
                ),
                callback_data=f"accept_payment_{from_user_id}",
            ),
            InlineKeyboardButton(
                text=localizer.get_user_localized_text(
                    user_language_code=language_code,
                    text_localization=localizer.button.reject,
                ),
                callback_data=f"reject_payment_{from_user_id}",
            ),
        ]
        keyboard.add(*buttons)

    additional_buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.delete_keyboard,
            ),
            callback_data="delete_keyboard",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.show_user,
            ),
            callback_data=f"show_user_{from_user_id}",
        ),
    ]
    for button in additional_buttons:
        keyboard.add(button)

    return keyboard


async def insert_button_back_to_main_menu(
    keyboard: InlineKeyboardMarkup | None = None, language_code: str = "ru"
):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.back_to_main_menu,
            ),
            callback_data="back_to_main_menu",
        )
    )
    return keyboard


async def user_configs_list_keyboard(
    user_id: int, language_code: str, show_create_new_config_button: bool = True
) -> InlineKeyboardMarkup:
    users_configs = await db_manager.get_user_config_names_and_uuids(user_id=user_id)
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    is_user_can_generate_new_config = (
        await db_manager.get_count_of_configs_user_can_create(user_id=user_id)
    ) > 0
    if is_user_can_generate_new_config and show_create_new_config_button:
        create_new_config_button = InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.create_new_config,
            ),
            callback_data="create_new_config",
        )
        keyboard.insert(create_new_config_button)

    if users_configs:
        exist_configs_buttons = [
            InlineKeyboardButton(
                text=config.config_name,
                callback_data=f"show_config_{config.config_uuid}",
            )
            for config in users_configs
        ]
        keyboard.add(*exist_configs_buttons)

    keyboard = await insert_button_back_to_main_menu(
        keyboard=keyboard, language_code=language_code
    )
    return keyboard


async def admin_support_question_notification_keyboard(
    question: str, from_user: str, language_code: str, answer: str | None = None
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(
        text=localizer.get_user_localized_text(
            user_language_code=language_code,
            text_localization=localizer.button.answer_to_user_as_support,
        ),
        callback_data=support_callback.new(
            question=question,
            from_user=from_user,
            answer=answer if answer else "NULL",
        ),
    )
    keyboard.insert(button)
    return keyboard


async def admin_user_info_keyboard(
    language_code: str, user_id: int
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.show_user_configs,
            ),
            callback_data=f"show_users_configs_{user_id}",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.give_bonus_configs,
            ),
            callback_data=f"give_bonus_configs_{user_id}",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.ban_user,
            ),
            callback_data=f"ban_user_{user_id}",
        ),
        InlineKeyboardButton(
            text=localizer.get_user_localized_text(
                user_language_code=language_code,
                text_localization=localizer.button.give_user_subscription,
            ),
            callback_data=f"give_subscription_{user_id}",
        ),
    ]
    keyboard.add(*buttons)
    keyboard = await insert_button_back_to_main_menu(
        keyboard=keyboard, language_code=language_code
    )

    return keyboard


async def delete_specified_config_keyboard(
    config_uuid: int, language_code: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(
        text=localizer.get_user_localized_text(
            user_language_code=language_code,
            text_localization=localizer.button.delete_config,
        ),
        callback_data=f"delete_config_{config_uuid}",
    )
    keyboard.insert(button)
    keyboard = await insert_button_back_to_main_menu(
        keyboard=keyboard, language_code=language_code
    )
    return keyboard


async def confirm_delete_config_keyboard(
    config_uuid: int, language_code: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(
        text=localizer.get_user_localized_text(
            user_language_code=language_code,
            text_localization=localizer.button.delete_config,
        ),
        callback_data=f"confirm_delete_config_{config_uuid}",
    )
    keyboard.insert(button)
    keyboard = await insert_button_back_to_main_menu(
        keyboard=keyboard, language_code=language_code
    )
    return keyboard
