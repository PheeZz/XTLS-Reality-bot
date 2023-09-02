from .localized_text_model import LocalizedText
from .base_localized_object import BaseLocalizedObject


class LocalizedButtonText(BaseLocalizedObject):
    """class with buttons localization from localization.json"""

    def __init__(
        self,
    ) -> None:
        super().__init__(entity_type="button")

    @property
    def pc(self) -> LocalizedText:
        return self._get_entity_text("pc")

    @property
    def mobile(self) -> LocalizedText:
        return self._get_entity_text("mobile")

    @property
    def my_configs(self) -> LocalizedText:
        return self._get_entity_text("my_configs")

    @property
    def my_subscription(self) -> LocalizedText:
        return self._get_entity_text("my_subscription")

    @property
    def show_user(self) -> LocalizedText:
        return self._get_entity_text("show_user")

    @property
    def show_user_configs(self) -> LocalizedText:
        return self._get_entity_text("show_user_configs")

    @property
    def give_user_subscription(self) -> LocalizedText:
        return self._get_entity_text("give_user_subscription")

    @property
    def take_user_subscription(self) -> LocalizedText:
        return self._get_entity_text("take_user_subscription")

    @property
    def show_statistics(self) -> LocalizedText:
        return self._get_entity_text("show_statistics")

    @property
    def accept(self) -> LocalizedText:
        return self._get_entity_text("accept")

    @property
    def reject(self) -> LocalizedText:
        return self._get_entity_text("reject")

    @property
    def delete_keyboard(self) -> LocalizedText:
        return self._get_entity_text("delete_keyboard")

    @property
    def create_new_config(self) -> LocalizedText:
        return self._get_entity_text("create_new_config")

    @property
    def back_to_main_menu(self) -> LocalizedText:
        return self._get_entity_text("back_to_main_menu")
