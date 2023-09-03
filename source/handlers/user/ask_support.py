from loguru import logger
from source.utils import localizer
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked

from source.keyboard import inline
from source.data import config
from source.utils.states.user import AskSupport

from source.middlewares import rate_limit


@rate_limit(limit=1)
async def ask_user_for_question_to_support(
    call: types.CallbackQuery, state: FSMContext
):
    await state.finish()
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.ask_support_question,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
    await AskSupport.waiting_for_question.set()


async def forward_question_to_admins(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.support_question_sent_by_user,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=message.from_user.language_code,
        ),
        parse_mode=types.ParseMode.HTML,
    )
    for admin_id in config.admins_ids:
        forwarded_message = await message.forward(admin_id)
        admin_user = (
            await message.bot.get_chat_member(chat_id=admin_id, user_id=admin_id)
        ).user
        try:
            await forwarded_message.reply(
                text=localizer.get_user_localized_text(
                    user_language_code=admin_user.language_code,
                    text_localization=localizer.message.admin_notification_about_new_support_question,
                ).format(
                    user_id=message.from_user.id,
                    username=message.from_user.username
                    if message.from_user.username
                    else message.from_user.full_name,
                ),
                parse_mode=types.ParseMode.HTML,
                reply_markup=await inline.admin_support_question_notification_keyboard(
                    language_code=admin_user.language_code,
                    from_user=message.from_user.id,
                    question=forwarded_message.text
                    if forwarded_message.text
                    else forwarded_message.caption,
                ),
            )
        except BotBlocked as e:
            logger.error(f"Bot blocked by admin {admin_id} - {e}")
