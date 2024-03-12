from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import BotBlocked
from loguru import logger

from source.data import config
from source.keyboard import inline
from source.middlewares import rate_limit
from source.utils import localizer
from source.utils.states.admin import AnswerSupport


@rate_limit(limit=1)
async def ask_admin_for_support_answer(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    await state.finish()
    await call.message.edit_text(
        text=localizer.get_user_localized_text(
            user_language_code=call.from_user.language_code,
            text_localization=localizer.message.ask_admin_for_support_answer,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=call.from_user.language_code,
        ),
    )
    question = callback_data.get("question")
    from_user_id = callback_data.get("from_user")
    await state.update_data(support_question=question, from_user_id=from_user_id)
    await AnswerSupport.wait_for_support_answer.set()


async def send_support_answer_to_user(message: types.Message, state: FSMContext):
    support_question = (await state.get_data()).get("support_question")
    question_from_user_id = (await state.get_data()).get("from_user_id")
    try:
        await message.bot.send_message(
            chat_id=question_from_user_id,
            text=localizer.get_user_localized_text(
                user_language_code=message.from_user.language_code,
                text_localization=localizer.message.support_answer_from_admin,
            ).format(
                support_question=support_question,
                support_answer=message.text,
            ),
            parse_mode=types.ParseMode.HTML,
        )
    except BotBlocked:
        logger.error(f"Bot blocked by user {question_from_user_id}")
        return
    await message.answer(
        text=localizer.get_user_localized_text(
            user_language_code=message.from_user.language_code,
            text_localization=localizer.message.support_answer_sent_to_user,
        ),
        reply_markup=await inline.insert_button_back_to_main_menu(
            language_code=message.from_user.language_code,
        ),
    )
    await state.finish()
