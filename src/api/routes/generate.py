from fastapi import APIRouter, HTTPException
from src.models.request import GenerateRequest
from src.models.response import GenerateResponse
from src.providers import YandexProvider, GigaChatProvider, OpenAIProvider
import time

router = APIRouter()

# Инициализация провайдеров
yandex = YandexProvider()
gigachat = GigaChatProvider()
openai = OpenAIProvider()


@router.post("/generate/{provider_name}")
async def generate(provider_name: str, request: GenerateRequest):
    start_time = time.time()

    try:
        if provider_name == "yandex":
            response_text, latency, tokens = await yandex.generate(
                prompt=request.prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider_name == "gigachat":
            response_text, latency, tokens = await gigachat.generate(
                prompt=request.prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        elif provider_name == "openai":
            response_text, latency, tokens = await openai.generate(
                prompt=request.prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        else:
            raise HTTPException(status_code=404, detail=f"Provider {provider_name} not found")

        total_latency = int((time.time() - start_time) * 1000)

        return GenerateResponse(
            prompt=request.prompt,
            response=response_text,
            provider=provider_name,
            model=request.model or getattr(openai, 'default_model', 'unknown'),
            latency_ms=total_latency,
            tokens_used=tokens if tokens else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare(request: dict):  # TODO: добавить CompareRequest модель
    """Сравнить несколько провайдеров на одном промпте"""
    prompt = request.get("prompt")
    providers_list = request.get("providers", ["yandex", "gigachat"])

    results = {}
    for provider in providers_list:
        try:
            resp = await generate(provider, GenerateRequest(prompt=prompt))
            results[provider] = resp.dict()
        except Exception as e:
            results[provider] = {"error": str(e)}

    return {"prompt": prompt, "results": results}