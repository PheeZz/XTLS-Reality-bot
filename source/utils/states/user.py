from aiogram.dispatcher.filters.state import StatesGroup, State


class PaymentViaBankTransfer(StatesGroup):
    waiting_for_payment_screenshot_or_receipt = State()


class GeneratingNewConfig(StatesGroup):
    waiting_for_config_name = State()


class AskSupport(StatesGroup):
    waiting_for_question = State()
