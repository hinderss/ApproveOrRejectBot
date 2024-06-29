import configparser


class Localization:
    default_language_code = 'en'

    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename, encoding='utf-8')

    def get(self, language, key, **kwargs) -> str:
        messages = self.config
        if language in messages and key in messages[language]:
            return messages[language][key].format(**kwargs)
        return '_'

    def get_language_code(self, user_code) -> str:
        available_languages = self.available_languages()
        if user_code in available_languages:
            return user_code
        return Localization.default_language_code

    def available_languages(self) -> list:
        languages = list(self.config.keys())
        if 'DEFAULT' in languages:
            languages.remove('DEFAULT')
        return languages

    def language_by_code(self, language_code, **kwargs) -> str:
        available_languages = self.available_languages()
        if language_code in available_languages and 'language' in self.config[language_code]:
            return self.config[language_code]['language'].format(**kwargs)
        return '🏳️ Unknown language'
