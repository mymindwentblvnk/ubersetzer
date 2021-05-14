from enum import Enum


class UbersetzerLanguage(Enum):
    GERMAN = 1
    ENGLISH = 2


class Ubersetzer(object):

    def __init__(self):
        pass

    def translate(self,
                  source_language: UbersetzerLanguage,
                  target_language: UbersetzerLanguage,
                  message: str) -> str:
        return message
