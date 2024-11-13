import json
from config import LANGUAGES


def load_translations():
    translations = {}
    for lang in LANGUAGES:
        with open(f"localization/{lang}.json", "r") as file:
            translations[lang] = json.load(file)
    return translations


translations = load_translations()


def get_text(key, language):
    return translations[language].get(key, key)
