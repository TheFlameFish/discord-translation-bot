import json
import os
import logging

logger: logging.Logger = None

# Note: Spanish localization is partially AI generated and could probably be improved.
# Currently, I've got English and Spanish.

locales = {
    "en-GB": "en",      "en-US": "en",
    "es-ES": "es",      # "es-419": "es", # Supposedly not a supported locale
    "fr": "fr",         "hr": "hr",
    "it": "it",         "lt": "lt",
    "hu": "hu",         "no": "no",
    "pl": "pl",         "pt-BR": "pt",
    "ro": "ro",         "fi": "fi",
    "sv-SE": "sv",      "vi": "vi",
    "tr": "tr",         "cs": "cs",
    "el": "el",         "bg": "bg",
    "ru": "ru",         "uk": "uk",
    "hi": "hi",         "th": "th",
    "zh-CN": "zh-CN",   "ja": "ja",
    "zh-TW": "zh-TW",   "ko": "ko",
}

localization = {}

def load(log: logging.Logger):
    global localization
    global logger
    for locale, file in locales.items():
        if not os.path.exists(f"resources/localization/{file}.json"):
            continue
        with open(f"resources/localization/{file}.json") as f:
            localization[locale] = json.load(f)
    logger = log.getChild(__name__)

    logger.info("Loaded localization data.")

def get_locale_dict(key: str, **kwargs):
    dict = {}

    for locale, data in localization.items():
        dict[locale] = data.get(key, key).format(**kwargs)
        
    logger.info(f"Generated locale dict for key '{key}': {dict}")

    return dict

def get(key: str, locale: str, **kwargs):
    if locale == "es-419":
        locale = "es-ES" # Supposedly es-419 is not a supported locale. 
                         # (Despite the fact that it is listed in their docs.)
    elif locale not in localization:
        logger.warn("Locale not available: ", locale)
        return localization["en-US"].get(key, key).format(**kwargs)

    return localization[locale].get(key, key).format(**kwargs)

