from loguru import logger
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from source.keyboard import inline
from source.data import config
from loader import db_manager


from source.middlewares import rate_limit


@rate_limit(limit=1)
async def start(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} started bot")
    await state.finish()

    await db_manager.upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username if message.from_user.username else None,
    )
    if not await db_manager.is_user_registered(user_id=message.from_user.id):
        new_user = True
    else:
        new_user = False
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.new_user_greeting
            if new_user
            else localizer.message.greeting,
        ).format(
            user=message.from_user.full_name,
            is_admin_access=hbold("[ADMIN ACCESS]\n\n")
            if message.from_user.id in config.admins_ids
            else "",
            server_country=config.server_country,
        ),
        reply_markup=await inline.start_menu_kb(
            language_code=message.from_user.language_code,
            user_id=message.from_user.id,
        ),
        parse_mode=types.ParseMode.HTML,
    )


@rate_limit(limit=1)
async def main_menu_by_button(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.greeting,
        ).format(
            user=call.from_user.full_name,
            is_admin_access=hbold(
                "[ADMIN ACCESS]\n\n",
            )
            if call.from_user.id in config.admins_ids
            else "",
            server_country=config.server_country,
        ),
        reply_markup=await inline.start_menu_kb(
            language_code=call.from_user.language_code,
            user_id=call.from_user.id,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    await call.answer()
