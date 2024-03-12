import json

from loguru import logger

from .localized_text_model import LocalizedText


class BaseLocalizedObject:
    def __init__(
        self,
        entity_type: str = "message",
        localization_path: str = "source/data/localization.json",
    ) -> None:
        self._entity_type = entity_type
        with open(localization_path, "r") as file:
            self._data: dict[str, dict[str, str]] = json.load(file)
        try:
            self._data = self._data[entity_type]
        except KeyError:
            raise KeyError(
                f"Key {entity_type} not found in localization.json. Available keys: {list(self._data.keys())}"
            )
        logger.info(f"Loaded [{entity_type}] localization")

    def _get_entity_text(self, entity: str) -> LocalizedText:
        entity_text: dict[str, str] = self._data.get(entity, {})
        if not entity_text:
            raise KeyError(
                f"Key {entity} not found in localization.json of type {self._entity_type}"
            )
        try:
            en_localization = entity_text["en"]
        except KeyError:
            raise KeyError(
                f"Key 'en' not found in localization.json for entity [{entity}] of type {self._entity_type}"
            )
        return LocalizedText(en=en_localization, ru=entity_text.get("ru", en_localization))
