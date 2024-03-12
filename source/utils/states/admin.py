from aiogram.dispatcher.filters.state import State, StatesGroup


class GetUserInfo(StatesGroup):
    wait_for_user_id_or_username = State()


class AnswerSupport(StatesGroup):
    wait_for_support_answer = State()


class GiveSubscription(StatesGroup):
    wait_for_subscription_duration = State()


class GiveBonusConfigGenerations(StatesGroup):
    wait_for_bonus_config_generations_count = State()
