import pytest
from src.services.translator import translator_service
from src.models.request import TranslateRequest
from src.models.request import Language


@pytest.mark.asyncio
async def test_translate_english_to_russian():
    request = TranslateRequest(
        text="Hello world",
        target_lang=Language.RUSSIAN
    )

    response = await translator_service.translate(request)

    assert response.original == "Hello world"
    assert response.target_lang == "ru"
    assert "привет" in response.translated.lower()
    assert isinstance(response.processing_time_ms, float)


@pytest.mark.asyncio
async def test_translate_caching():
    request = TranslateRequest(
        text="Test cache",
        target_lang=Language.FRENCH
    )

    # First request - cache miss
    response1 = await translator_service.translate(request)
    assert response1.cache_hit is False

    # Second request - cache hit
    response2 = await translator_service.translate(request)
    assert response2.cache_hit is True
    assert response1.translated == response2.translated


@pytest.mark.asyncio
async def test_batch_translate():
    texts = ["Hello", "Goodbye", "Thank you"]
    target = Language.SPANISH

    responses = await translator_service.batch_translate(texts, target)

    assert len(responses) == 3
    for response in responses:
        assert response.target_lang == "es"