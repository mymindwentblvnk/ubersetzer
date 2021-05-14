from enum import Enum

from googletrans import Translator


class UbersetzerLanguage(Enum):
    GERMAN = 'de'
    ENGLISH = 'en'


class Ubersetzer(object):

    def __init__(self):
        pass

    def translate(self,
                  source_language: UbersetzerLanguage,
                  target_language: UbersetzerLanguage,
                  message: str) -> str:
        return Translator().translate(message).text
