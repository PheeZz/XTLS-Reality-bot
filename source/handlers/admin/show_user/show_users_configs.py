from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db_manager
from source.keyboard import inline
from source.middlewares import rate_limit
from source.utils import localizer


@rate_limit(limit=1)
async def switch_keyboard_to_user_configs(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split("_")[-1]
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.user_configs_list,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.user_configs_list_keyboard(
            user_id=user_id,
            language_code=call.from_user.language_code,
            show_create_new_config_button=False,
        ),
    )
