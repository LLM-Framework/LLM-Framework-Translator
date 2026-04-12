from fastapi import APIRouter
from src.services.translator import translator_service
from src.models.response import CacheStatsResponse

router = APIRouter()

@router.get("/cache/stats", response_model=CacheStatsResponse)
async def get_cache_stats():
    """Get cache statistics"""
    stats = translator_service.get_cache_stats()
    return CacheStatsResponse(**stats)

@router.delete("/cache")
async def clear_cache():
    """Clear translation cache"""
    translator_service.clear_cache()
    return {"status": "cleared", "message": "Cache cleared successfully"}