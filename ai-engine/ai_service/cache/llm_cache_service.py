import hashlib

class LLMCacheService:

    def __init__(self):
        self._cache: dict[str, dict] = {}

    def _build_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def get(self, prompt: str):

        key = self._build_key(prompt)
        return self._cache.get(key)

    def set(self, prompt: str, value: dict):

        key = self._build_key(prompt)
        self._cache[key] = value