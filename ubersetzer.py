from enum import Enum

from googletrans import Translator


translator = Translator()


class Language(Enum):
    GERMAN = {'iso': 'de', 'slack-reaction': 'de'}
    ENGLISH = {'iso': 'en', 'slack-reaction': 'gb'}
    DUTCH = {'iso': 'nl', 'slack-reaction': 'flag-nl'}


class Ubersetzer(object):

    def __init__(self):
        pass

    def translate(self, message: str, target_language: Language) -> str:
        translation = translator.translate(message, dest=target_language.value['iso'])
        return translation.text
