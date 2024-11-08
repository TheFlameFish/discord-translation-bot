from deep_translator import GoogleTranslator as _GoogleTranslator
import json
import logging

from src.translation.translator import Translator

class GoogleTranslator(Translator):
    def __init__(self,logger: logging.Logger, langs_path="resources/langs_GT.json"):
        self.langs_path = langs_path
        self.logger = logger.getChild(__name__)

    def get_lang(self, lang: str) -> str:
        '''Takes a language code or full name and returns the language code'''
        with open(self.langs_path) as f:
            langs = json.load(f)
    
        if lang in langs:
            return lang
        
        lang = lang.lower()
        
        # Search for full language name or aliases
        for code, details in langs.items():
            if lang == details["full"].lower() or lang == details["full_en"].lower() or lang in [alias.lower() for alias in details.get("aliases", [])]:
                return code

        return None

    def get_from_emoji(self, emoji: str) -> str:
        '''Finds a language by its associated emoji.'''
        self.logger.info(f"Looking up language for emoji: {emoji}")
        with open(self.langs_path) as f:
            langs = json.load(f)

        # Iterate through the languages and their flags
        for lang, data in langs.items():
            if emoji in data.get("flags", []):  # Check if the emoji is in the flags list
                self.logger.info(f"Found language '{lang}' for emoji '{emoji}'")
                return lang
                
        self.logger.info(f"No language found for emoji: {emoji}")
        return None
    
    def translate(self, text: str, target_language: str, source_language: str = None) -> str:
        '''Translates text to a target language.'''
        lang = self.get_lang(target_language)

        if lang:
            # Use the existing instance (self) to call translate method on GoogleTranslator
            translator = _GoogleTranslator(source='auto', target=lang)
            return translator.translate(text)
        
        return None
