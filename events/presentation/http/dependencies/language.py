from fastapi import Request, Depends

from events.main.config import Config


class LanguageValidator:
    def __init__(self, config: Config):
        self.supported_languages = config.app.supported_languages

    async def __call__(self, request: Request) -> str:
        language = request.headers.get("Accept-Language", "en")
        if language not in self.supported_languages:
            return "en"
        return language


def get_valid_language(
    validator: LanguageValidator = Depends(LanguageValidator(Config()))
) -> LanguageValidator:
    return validator
