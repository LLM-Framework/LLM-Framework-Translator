from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
from datetime import datetime

from src.api.routes import translate, batch, languages, cache
from src.config import settings
from src.models.response import HealthResponse

app = FastAPI(
    title="LLM Translator Service",
    description="Мультиязычный перевод для тестирования промпт-инъекций в LLM",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-MS"] = str(round(process_time, 2))
    return response

# Include routers
app.include_router(translate.router, prefix="/api/v1", tags=["Translation"])
app.include_router(batch.router, prefix="/api/v1", tags=["Batch"])
app.include_router(languages.router, prefix="/api/v1", tags=["Languages"])
app.include_router(cache.router, prefix="/api/v1", tags=["Cache"])

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        service="translator",
        version="1.0.0",
        timestamp=datetime.now()
    )

@app.get("/")
async def root():
    return {
        "service": "LLM Translator Service",
        "version": "1.0.0",
        "docs": "/docs" if settings.debug else "disabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.translator_host,
        port=settings.translator_port,
        reload=settings.debug
    )