from dataclasses import dataclass
from enum import Enum

from googletrans import Translator


translator = Translator()


@dataclass
class LanguageData(object):
    iso: str
    emoji: str
    language: str
    flag_emoji: str


class Language(Enum):
    # Supported languages: https://cloud.google.com/translate/docs/languages
    GERMAN = LanguageData(iso='de', emoji='pls-translate-to-de', language='German', flag_emoji='flag-de')
    ENGLISH = LanguageData(iso='en', emoji='pls-translate-to-en', language='English', flag_emoji='flag-gb')
    SERBIAN = LanguageData(iso='sr', emoji='pls-translate-to-sr', language='Serbian', flag_emoji='flag-rs')
    BOSNIAN = LanguageData(iso='bs', emoji='pls-translate-to-bs', language='Bosnian', flag_emoji='flag-ba')
    CROATIAN = LanguageData(iso='hr', emoji='pls-translate-to-hr', language='Croatian', flag_emoji='flag-hr')
    DUTCH = LanguageData(iso='nl', emoji='pls-translate-to-nl', language='Dutch', flag_emoji='flag-nl')


class Ubersetzer(object):

    def __init__(self):
        pass

    def translate(self, message: str, target_language: Language) -> str:
        translation = translator.translate(message,
                                           dest=target_language.value.iso)
        return translation.text
