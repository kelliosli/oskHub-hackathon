import json

LANGUAGES = ("en", "kz", "ru")


def load_translations():
    translations = {}
    for lang in LANGUAGES:
        with open(f"locales/{lang}.json", "r") as file:
            translations[lang] = json.load(file)
    return translations


translations = load_translations()


def get_text(key, language):
    return translations[language].get(key, key)


def get_key_and_lang(text):
    # Loop through each language's translation dictionary
    for lang in LANGUAGES:
        for key, value in translations[lang].items():
            if value == text:
                return key, lang
    # Return None if text not found in translations
    return None
