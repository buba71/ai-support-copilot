import hashlib
import json
import redis
from typing import Optional

class LLMCacheService:
    def __init__(self, redis_client: redis.Redis, ttl: int = 86400):
        """
        Shared cache using Redis.
        :param redis_client: Redis client connection
        :param ttl: Time To Live in seconds (default: 24h)
        """
        self.redis = redis_client
        self.ttl = ttl
        self.prefix = "llm_cache:"
        self.hits_key = f"{self.prefix}stats:hits"
        self.misses_key = f"{self.prefix}stats:misses"

    def _build_key(self, prompt: str) -> str:
        hashed_prompt = hashlib.sha256(prompt.encode()).hexdigest()
        return f"{self.prefix}{hashed_prompt}"

    def get(self, prompt: str) -> Optional[dict]:
        key = self._build_key(prompt)
        value = self.redis.get(key)

        if value:
            self.redis.incr(self.hits_key)
            return json.loads(value)
        
        self.redis.incr(self.misses_key)
        return None

    def set(self, prompt: str, value: dict):
        key = self._build_key(prompt)
        # Serialize dict to JSON string before storing in Redis
        self.redis.set(key, json.dumps(value), ex=self.ttl)

    def efficiency(self) -> float:
        """
        Calculates global efficiency from Redis counters.
        """
        hits = int(self.redis.get(self.hits_key) or 0)
        misses = int(self.redis.get(self.misses_key) or 0)
        total = hits + misses

        if total == 0:
            return 0.0

        return round(hits / total, 3)