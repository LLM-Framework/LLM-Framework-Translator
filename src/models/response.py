from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class TranslateResponse(BaseModel):
    original: str
    translated: str
    target_lang: str
    cache_hit: bool
    processing_time_ms: float

class BatchTranslateResponse(BaseModel):
    results: List[TranslateResponse]
    total_time_ms: float

class LanguageInfo(BaseModel):
    code: str
    name: str
    native_name: str

class LanguagesResponse(BaseModel):
    languages: Dict[str, LanguageInfo]

class CacheStatsResponse(BaseModel):
    size: int
    max_size: int
    hit_rate: float
    miss_rate: float

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime