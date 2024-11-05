import json
import os

# Note: Spanish localization is partially AI generated and could probably be improved.
# Currently, I've got English and Spanish.

locales = {
    "en-GB": "en",      "en-US": "en",
    "es-ES": "es",      
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

def load():
    global localization
    for locale, file in locales.items():
        if not os.path.exists(f"localization/{file}.json"):
            continue
        with open(f"localization/{file}.json") as f:
            localization[locale] = json.load(f)

def get_locale_dict(key: str, **kwargs):
    dict = {}

    for locale, data in localization.items():
        dict[locale] = data.get(key, key).format(**kwargs)
        

    return dict

def get(key: str, locale: str, **kwargs):
    if locale not in localization:
        return localization["en"].get(key, key).format(**kwargs)

    return localization[locale].get(key, key).format(**kwargs)