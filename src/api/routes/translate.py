from fastapi import APIRouter, Depends
from src.models.request import TranslateRequest
from src.models.response import TranslateResponse
from src.services.translator import translator_service
from src.api.dependencies.rate_limiter import rate_limiter

router = APIRouter()

@router.post("/translate", response_model=TranslateResponse)
async def translate(
    request: TranslateRequest,
    _=Depends(rate_limiter)
):
    """Translate text from one language to another"""
    return await translator_service.translate(request)