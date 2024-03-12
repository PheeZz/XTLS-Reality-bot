from aiogram import types

from source.keyboard import inline
from source.middlewares import rate_limit
from source.utils import localizer


@rate_limit(limit=1)
async def show_help_guide(message: types.Message):
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.help_guide_select_device,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.help_guide_keyboard(
            language_code=message.from_user.language_code,
        ),
    )
