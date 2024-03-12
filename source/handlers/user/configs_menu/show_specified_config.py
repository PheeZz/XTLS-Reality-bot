from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db_manager
from source.keyboard import inline
from source.utils import localizer
from source.utils.qr_generator import create_qr_code_from_config_as_link_str
from source.utils.xray import xray_config


async def show_specified_config(call: types.CallbackQuery, state: FSMContext):
    config_uuid = call.data.split("_")[-1]
    config_name = await db_manager.get_config_name_by_config_uuid(config_uuid=config_uuid)
    config_as_link_str = await xray_config.create_user_config_as_link_string(
        uuid=config_uuid,
        config_name=config_name,
    )
    config_qr_code = create_qr_code_from_config_as_link_str(config=config_as_link_str)
    await call.message.answer_photo(
        photo=config_qr_code,
        caption=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.config_generated,
        ).format(config_name=config_name, config_data=config_as_link_str),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.delete_specified_config_keyboard(
            config_uuid=config_uuid, language_code=call.from_user.language_code
        ),
    )
