from source.utils import localizer
from aiogram import types

from source.middlewares import rate_limit
from source.keyboard import inline
from source.utils.guide_images_loader import GuideImagesLoader


@rate_limit(limit=1)
async def show_help_guide_ios(call: types.CallbackQuery):
    guide_images = await GuideImagesLoader().get_ios_guide_images()
    media_group = [types.InputMediaPhoto(media=photo) for photo in guide_images]

    await call.message.answer_media_group(
        media=media_group,
    )

    await call.message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.help_guide_ios,
        ),
        parse_mode=types.ParseMode.HTML,
        reply_markup=await inline.download_app_for_connect_to_vpn_keyboard(
            language_code=call.from_user.language_code,
            platform="ios",
        ),
    )
