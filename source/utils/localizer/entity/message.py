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

    @property
    def user_configs_list(self) -> LocalizedText:
        return self._get_entity_text("user_configs_list")

    @property
    def no_configs_found_create_new_one(self) -> LocalizedText:
        return self._get_entity_text("no_configs_found_create_new_one")

    @property
    def request_config_name(self) -> LocalizedText:
        return self._get_entity_text("request_config_name")

    @property
    def got_config_name_start_generating(self) -> LocalizedText:
        return self._get_entity_text("got_config_name_start_generating")

    @property
    def config_generated(self) -> LocalizedText:
        return self._get_entity_text("config_generated")

    @property
    def subscription_expired_notification(self) -> LocalizedText:
        return self._get_entity_text("subscription_expired_notification")

    @property
    def subscription_last_day_left_notification(self) -> LocalizedText:
        return self._get_entity_text("subscription_last_day_left_notification")

    @property
    def subscription_two_days_left_notification(self) -> LocalizedText:
        return self._get_entity_text("subscription_two_days_left_notification")
