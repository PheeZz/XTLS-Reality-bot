from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from loader import db_manager


async def show_info_about_user_by_button(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[-1]
    if not user_id:
        await request_user_id_or_username(call=call)
    user = await db_manager.get_user_by_id(user_id=user_id)
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.user_info,
        ).format(
            user_id=user_id,
            user_username=user.username,
            is_not_banned=user.is_not_banned,
            is_active_subscription=user.is_active_subscription,
            subscription_end_date=user.subscription_end_date.strftime("%d.%m.%Y"),
            configs_count=user.configs_count,
            bonus_configs_count=user.bonus_configs_count,
            unused_configs_count=user.unused_configs_count,
            created_at=user.created_at.strftime("%d.%m.%Y %H:%M:%S"),
        ),
        parse_mode=types.ParseMode.HTML,
        # reply_markup=await inline.admin_user_info_keyboard(
        #     language_code=call.from_user.language_code,
        #     user_id=user_id,
        # ),
    )


async def request_user_id_or_username(call: types.CallbackQuery):
    ...
