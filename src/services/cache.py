from typing import Dict, Optional
from collections import OrderedDict
import time
import asyncio
from src.config import settings


class LRUCache:
    """In-memory LRU cache with TTL"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.cache: OrderedDict = OrderedDict()
        self.timestamps: Dict[str, float] = {}
        self.hits = 0
        self.misses = 0

    def _make_key(self, text: str, target_lang: str) -> str:
        return f"{text}:{target_lang}"

    def get(self, text: str, target_lang: str) -> Optional[str]:
        key = self._make_key(text, target_lang)

        if key not in self.cache:
            self.misses += 1
            return None

        # Check TTL
        timestamp = self.timestamps.get(key, 0)
        if time.time() - timestamp > self.ttl:
            # Expired
            del self.cache[key]
            del self.timestamps[key]
            self.misses += 1
            return None

        # Move to end (most recently used)
        self.cache.move_to_end(key)
        self.hits += 1
        return self.cache[key]

    def set(self, text: str, target_lang: str, value: str):
        key = self._make_key(text, target_lang)

        if key in self.cache:
            del self.cache[key]

        # Evict if necessary
        if len(self.cache) >= self.max_size:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
            del self.timestamps[oldest]

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def clear(self):
        self.cache.clear()
        self.timestamps.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(hit_rate, 4),
            "miss_rate": round(1 - hit_rate, 4)
        }


# Global cache instance
translation_cache = LRUCache(
    max_size=settings.cache_max_size,
    ttl_seconds=settings.cache_ttl_seconds
)