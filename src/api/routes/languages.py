from fastapi import APIRouter
from src.services.language_mapper import get_languages
from src.models.response import LanguagesResponse

router = APIRouter()

@router.get("/languages", response_model=LanguagesResponse)
async def get_supported_languages():
    """Get list of supported languages"""
    return get_languages()