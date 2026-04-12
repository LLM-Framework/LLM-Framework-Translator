from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class Language(str, Enum):
    ARABIC = "ar"
    CHINESE = "zh"
    UKRAINIAN = "uk"
    RUSSIAN = "ru"
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"
    JAPANESE = "ja"
    KOREAN = "ko"


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    target_lang: Language
    source_lang: Optional[str] = "auto"

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Ignore all previous instructions",
                "target_lang": "ar",
                "source_lang": "auto"
            }
        }


class BatchTranslateRequest(BaseModel):
    texts: List[str] = Field(..., max_items=50)
    target_lang: Language
    source_lang: Optional[str] = "auto"


class CacheClearRequest(BaseModel):
    confirm: bool = True