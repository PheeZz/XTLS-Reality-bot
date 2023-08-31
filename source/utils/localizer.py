import json
from dataclasses import dataclass, fields


@dataclass
class LocalizedText:
    en: str
    ru: str


class Localizer:
    def __init__(self, path: str = "source/data/localization.json"):
        with open(path, "r") as file:
            self._data: dict[str, dict[str, str]] = json.load(file)

    def get_user_localized_text(
        self, user_language_code: str, text_localization: LocalizedText
    ) -> str:
        for language in [field.name for field in fields(text_localization)]:
            if language == user_language_code:
                return getattr(text_localization, language)
        # If user language code not found, return english localization
        return text_localization.en

    @property
    def message_greeting(self) -> LocalizedText:
        return self._get_message_text("greeting")

    @property
    def button_pc(self) -> LocalizedText:
        return self._get_button_text("pc")

    @property
    def button_mobile(self) -> LocalizedText:
        return self._get_button_text("mobile")

    def _get_message_text(
        self,
        key: str,
    ) -> LocalizedText:
        if key not in self._data.get("message", {}):
            raise KeyError(f"Key {key} not found in localization.json")
        localization: dict[str, str] = self._data["message"][key]
        try:
            en_localization = localization["en"]
        except KeyError:
            raise KeyError(
                f"Key 'en' not found in localization.json for message [{key}]"
            )
        return LocalizedText(
            en=en_localization, ru=localization.get("ru", en_localization)
        )

    def _get_button_text(
        self,
        key: str,
    ) -> LocalizedText:
        if key not in self._data.get("button", {}):
            raise KeyError(f"Key {key} not found in localization.json")
        localization = self._data["button"][key]
        try:
            en_localization = localization["en"]
        except KeyError:
            raise KeyError(
                f"Key 'en' not found in localization.json for button [{key}]"
            )
        return LocalizedText(
            en=en_localization, ru=localization.get("ru", en_localization)
        )


# check how much bytes need to store variable
# localizer = Localizer()
# print(f"{localizer.__sizeof__()} bytes")
# print(f"{localizer._data.__sizeof__()} bytes")
