from dataclasses import fields

from .entity import LocalizedText, LocalizedButtonText, LocalizedMessageText


class Localizer:
    def __init__(self):
        self.button = LocalizedButtonText()
        self.message = LocalizedMessageText()

    def get_user_localized_text(
        self, user_language_code: str, text_localization: LocalizedText
    ) -> str:
        for language in [field.name for field in fields(text_localization)]:
            if language == user_language_code:
                return getattr(text_localization, language)
        # If user language code not found, return english localization
        return text_localization.en


if __name__ == "__main__":
    # check how much bytes need to store variable
    localizer = Localizer()
    print(f"{localizer.__sizeof__()} bytes")
    print(f"{localizer._data.__sizeof__()} bytes")
