from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from source.utils import localizer

from loader import db_manager


async def show_global_stats(call: types.CallbackQuery, state: FSMContext):
    global_stats = await db_manager.get_global_stats()
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.global_stats,
        ).format(
            users_registered=global_stats.users_registered,
            users_banned=global_stats.users_banned,
            users_with_active_subscription=global_stats.users_with_active_subscription,
            users_with_expired_subscription=global_stats.users_with_expired_subscription,
            users_with_last_day_left_subscription=global_stats.users_with_last_day_left_subscription,
            users_with_two_days_left_subscription=global_stats.users_with_two_days_left_subscription,
            active_configs_count=global_stats.active_configs_count,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
