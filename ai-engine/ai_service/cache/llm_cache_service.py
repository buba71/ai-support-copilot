import hashlib

class LLMCacheService:

    def __init__(self):
        self._cache: dict[str, dict] = {}
        self.hits = 0
        self.misses = 0

    def _build_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str):

        key = self._build_key(prompt)

        value = self._cache.get(key)

        if value:
            self.hits += 1
        else:
            self.misses += 1

        return value

    def set(self, prompt: str, value: dict):

        key = self._build_key(prompt)

        self._cache[key] = value

    def efficiency(self):

        total = self.hits + self.misses

        if total == 0:
            return 0

        return round(self.hits / total, 3)