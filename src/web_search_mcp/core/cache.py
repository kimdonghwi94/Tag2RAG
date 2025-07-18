import redis.asyncio as redis
import json
from ..config import settings

class RedisCache:
    def __init__(self, host, port):
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    async def get(self, key: str):
        cached_data = await self.client.get(key)
        if cached_data:
            return json.loads(cached_data)
        return None

    async def set(self, key: str, value, expire: int = 3600):
        await self.client.set(key, json.dumps(value), ex=expire)

redis_cache = RedisCache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)