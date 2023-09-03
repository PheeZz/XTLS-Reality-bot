from aiogram.dispatcher.filters.state import StatesGroup, State


class GetUserInfo(StatesGroup):
    wait_for_user_id_or_username = State()


class AnswerSupport(StatesGroup):
    wait_for_support_answer = State()
