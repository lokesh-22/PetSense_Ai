import json

from app.core.config import settings

try:
    from redis import Redis
except ImportError:  # pragma: no cover
    Redis = None


class CacheService:
    def __init__(self) -> None:
        self.client = None
        if Redis is not None:
            try:
                self.client = Redis.from_url(settings.redis_url, decode_responses=True)
            except Exception:
                self.client = None

    def get_json(self, key: str):
        if not self.client:
            return None
        try:
            raw = self.client.get(key)
        except Exception:
            return None
        return json.loads(raw) if raw else None

    def set_json(self, key: str, value, ttl_seconds: int = 3600) -> None:
        if not self.client:
            return
        try:
            self.client.setex(key, ttl_seconds, json.dumps(value))
        except Exception:
            return


cache_service = CacheService()
