from .localized_text_model import LocalizedText
from .base_localized_object import BaseLocalizedObject


class LocalizedMessageText(BaseLocalizedObject):
    """class with messages localization from localization.json"""

    def __init__(
        self,
    ) -> None:
        super().__init__(entity_type="message")

    @property
    def new_user_greeting(self) -> LocalizedText:
        return self._get_entity_text("new_user_greeting")

    @property
    def greeting(self) -> LocalizedText:
        return self._get_entity_text("greeting")

    @property
    def payment_method_card(self) -> LocalizedText:
        return self._get_entity_text("payment_method_card")

    @property
    def payment_method_card_success(self) -> LocalizedText:
        return self._get_entity_text("payment_method_card_success")

    @property
    def admin_notification_about_new_payment(self) -> LocalizedText:
        return self._get_entity_text("admin_notification_about_new_payment")

    @property
    def payment_accepted_for_admin(self) -> LocalizedText:
        return self._get_entity_text("payment_accepted_for_admin")

    @property
    def payment_accepted_for_user(self) -> LocalizedText:
        return self._get_entity_text("payment_accepted_for_user")

    @property
    def error_while_accepting_payment(self) -> LocalizedText:
        return self._get_entity_text("error_while_accepting_payment")

    @property
    def reject_payment(self) -> LocalizedText:
        return self._get_entity_text("reject_payment")

    @property
    def user_info(self) -> LocalizedText:
        return self._get_entity_text("user_info")
