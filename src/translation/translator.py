from abc import ABC, abstractmethod

class Translator():
    @abstractmethod
    def get_lang(self, lang: str) -> str:
        '''Takes a language code or full name and returns the language code'''
        pass

    @abstractmethod
    def get_from_emoji(self, emoji: str) -> str:
        '''Finds a language by its associated emoji.'''
        pass

    @abstractmethod
    def translate(self, text: str, target_language: str, source_language: str = None) -> str:
        '''Translates text to a target language.'''
        pass