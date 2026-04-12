from deep_translator import GoogleTranslator
import time
import asyncio
from typing import Optional
from src.services.cache import translation_cache
from src.models.request import TranslateRequest
from src.models.response import TranslateResponse
from src.config import settings


class TranslatorService:
    def __init__(self):
        self.cache = translation_cache

    async def translate(self, request: TranslateRequest) -> TranslateResponse:
        start_time = time.time()

        # Check cache first
        cached = self.cache.get(request.text, request.target_lang.value)
        if cached:
            processing_time = (time.time() - start_time) * 1000
            return TranslateResponse(
                original=request.text,
                translated=cached,
                target_lang=request.target_lang.value,
                cache_hit=True,
                processing_time_ms=round(processing_time, 2)
            )

        # Perform translation
        try:
            # Run in thread pool because GoogleTranslator is sync
            translator = await asyncio.to_thread(
                GoogleTranslator,
                source=request.source_lang,
                target=request.target_lang.value
            )

            translated = await asyncio.to_thread(
                translator.translate,
                request.text
            )

            # Save to cache
            self.cache.set(request.text, request.target_lang.value, translated)

            processing_time = (time.time() - start_time) * 1000
            return TranslateResponse(
                original=request.text,
                translated=translated,
                target_lang=request.target_lang.value,
                cache_hit=False,
                processing_time_ms=round(processing_time, 2)
            )

        except Exception as e:
            # Fallback: return original text on error
            processing_time = (time.time() - start_time) * 1000
            return TranslateResponse(
                original=request.text,
                translated=request.text,
                target_lang=request.target_lang.value,
                cache_hit=False,
                processing_time_ms=round(processing_time, 2)
            )

    async def batch_translate(self, texts: list, target_lang: str) -> list:
        tasks = [
            self.translate(TranslateRequest(text=t, target_lang=target_lang))
            for t in texts
        ]
        return await asyncio.gather(*tasks)

    def get_cache_stats(self) -> dict:
        return self.cache.get_stats()

    def clear_cache(self):
        self.cache.clear()


# Global service instance
translator_service = TranslatorService()