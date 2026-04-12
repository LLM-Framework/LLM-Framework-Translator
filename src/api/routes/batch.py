from fastapi import APIRouter, Depends
from src.models.request import BatchTranslateRequest
from src.models.response import BatchTranslateResponse
from src.services.translator import translator_service
from src.api.dependencies.rate_limiter import rate_limiter
import time

router = APIRouter()


@router.post("/batch", response_model=BatchTranslateResponse)
async def batch_translate(
        request: BatchTranslateRequest,
        _=Depends(rate_limiter)
):
    """Batch translate multiple texts"""
    start_time = time.time()

    results = await translator_service.batch_translate(
        texts=request.texts,
        target_lang=request.target_lang.value
    )

    total_time = (time.time() - start_time) * 1000

    return BatchTranslateResponse(
        results=results,
        total_time_ms=round(total_time, 2)
    )