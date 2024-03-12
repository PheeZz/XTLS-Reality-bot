from aiogram import types
from aiogram.dispatcher import FSMContext

from source.keyboard import inline
from source.middlewares import rate_limit
from source.utils import localizer
from source.utils.xray import xray_config


@rate_limit(limit=1)
async def confirm_delete_config(call: types.CallbackQuery, state: FSMContext):
    config_uuid = call.data.split("_")[-1]
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.confirm_delete_config,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.confirm_delete_config_keyboard(
            config_uuid=config_uuid, language_code=call.from_user.language_code
        ),
    )


async def delete_config(call: types.CallbackQuery, state: FSMContext):
    config_uuid = call.data.split("_")[-1]
    await xray_config.disconnect_user_by_uuid(uuid=config_uuid)
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.config_deleted,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    await call.answer()
    await call.message.delete()
    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.user_configs_list,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.user_configs_list_keyboard(
            user_id=call.from_user.id,
            language_code=call.from_user.language_code,
            show_create_new_config_button=True,
        ),
    )
    await state.finish()
