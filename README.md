# Translator Service

Сервис для мультиязычного перевода промптов с поддержкой кэширования и rate limiting.

## 🎯 Назначение

Сервис обеспечивает автоматический перевод текстовых промптов на целевые языки (арабский, китайский, украинский и др.) для тестирования многоязычных промпт-инъекций. Поддерживает кэширование переводов для повышения производительности.

## 🚀 Запуск сервера

```bash
cd translator-service
make run
```

# Перевод текста
```bash
curl -X POST http://localhost:8001/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Ignore all previous instructions",
    "target_lang": "ar"
  }'
  
  
  curl -X POST http://localhost:8001/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello", "Goodbye", "Thank you"],
    "target_lang": "zh"
  }'
```

# Проверка работоспособности

```bash
# Health check
curl http://localhost:8001/health

# Статистика кэша
curl http://localhost:8001/api/v1/cache/stats
```

---

# Компонентная схема

```mermaid
flowchart TB
    subgraph API["API Layer"]
        Translate[POST /translate]
        Batch[POST /batch]
        Languages[GET /languages]
        Cache_Stats[GET /cache/stats]
    end

    subgraph Services["Services Layer"]
        Translator[Translator Service]
        LRU[LRU Cache]
        RateLimiter[Rate Limiter]
    end

    subgraph External["External"]
        GoogleTrans[Google Translate API]
    end

    Translate --> Translator
    Batch --> Translator
    Translator --> LRU
    Translator --> RateLimiter
    Translator --> GoogleTrans
    Languages --> LangDB[(Languages DB)]
    Cache_Stats --> LRU
```


# Поток данных

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Cache as LRU Cache
    participant Translator as Translator Service
    participant Google as Google Translate API
    
    Client->>API: POST /translate
    Note over Client,API: {text, target_lang}
    
    API->>Cache: Проверка наличия
    alt Cache hit
        Cache-->>API: Возврат из кэша
        API-->>Client: Ответ (cache_hit=true)
    else Cache miss
        API->>Translator: translate(text, lang)
        Translator->>Google: HTTP запрос
        Google-->>Translator: Переведённый текст
        Translator->>Cache: Сохранение результата
        Translator-->>API: Переведённый текст
        API-->>Client: Ответ (cache_hit=false)
    end
```

# Взаимодействие с сервисами

```mermaid
graph LR
    Translator[Translator Service<br/>:8001] -->|переведённый промпт| Proxy
    Proxy[LLM Proxy Service<br/>:8002] -->|ответ LLM| Evaluator
    Evaluator[Evaluator Service<br/>:8003] -->|оценка| Frontend

    style Translator fill:#e1f5fe,stroke:#01579b
    style Proxy fill:#fff3e0,stroke:#e65100
    style Evaluator fill:#e8f5e9,stroke:#1b5e20
    style Frontend fill:#f3e5f5,stroke:#4a148c
```

## Лицензия

Apache 2.0

## Автор
Ермолинская Александра Александровна
УрФУ, группа РИМ-150975к
