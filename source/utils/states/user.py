from aiogram.dispatcher.filters.state import StatesGroup, State


class PaymentViaBankTransfer(StatesGroup):
    waiting_for_payment_screenshot_or_receipt = State()
