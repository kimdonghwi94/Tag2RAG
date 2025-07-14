"""Redis client helper."""

import os
import redis.asyncio as redis


def get_redis() -> redis.Redis:
    """Return a Redis client using the ``REDIS_URL`` environment variable."""
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url)
