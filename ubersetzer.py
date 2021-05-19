from dataclasses import dataclass
from enum import Enum

from googletrans import Translator


translator = Translator()


@dataclass
class LanguageData(object):
    iso: str
    emoji: str


class Language(Enum):
    GERMAN = LanguageData(iso='de', emoji='pls-translate-to-de')
    ENGLISH = LanguageData(iso='en', emoji='pls-translate-to-en')
    DUTCH = LanguageData(iso='nl', emoji='pls-translate-to-nl')


class Ubersetzer(object):

    def __init__(self):
        pass

    def translate(self, message: str, target_language: Language) -> str:
        translation = translator.translate(message,
                                           dest=target_language.value.iso)
        return translation.text
