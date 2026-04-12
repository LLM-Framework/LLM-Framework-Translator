from src.models.response import LanguageInfo, LanguagesResponse

LANGUAGES = {
    "ar": LanguageInfo(code="ar", name="Arabic", native_name="العربية"),
    "zh": LanguageInfo(code="zh", name="Chinese", native_name="中文"),
    "uk": LanguageInfo(code="uk", name="Ukrainian", native_name="Українська"),
    "ru": LanguageInfo(code="ru", name="Russian", native_name="Русский"),
    "en": LanguageInfo(code="en", name="English", native_name="English"),
    "fr": LanguageInfo(code="fr", name="French", native_name="Français"),
    "es": LanguageInfo(code="es", name="Spanish", native_name="Español"),
    "de": LanguageInfo(code="de", name="German", native_name="Deutsch"),
    "ja": LanguageInfo(code="ja", name="Japanese", native_name="日本語"),
    "ko": LanguageInfo(code="ko", name="Korean", native_name="한국어"),
}

def get_languages() -> LanguagesResponse:
    return LanguagesResponse(languages=LANGUAGES)

def is_supported(lang_code: str) -> bool:
    return lang_code in LANGUAGES