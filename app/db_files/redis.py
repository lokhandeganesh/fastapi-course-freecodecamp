import redis.asyncio as redis
from app.db_files.config import settings

# Initialize a global variable for the pool
redis_client: redis.Redis = None


async def init_redis():
    """Initialize the Redis connection pool."""
    global redis_client
    redis_client = redis.from_url(
        url=settings.redis_url,
        encoding="utf-8",
        # Automatically decodes bytes to strings
        decode_responses=settings.redis_decode_response
    )


async def close_redis():
    """Close the Redis connection pool."""
    if redis_client:
        await redis_client.close()


async def get_redis():
    """Dependency for routers to get the Redis client."""
    return redis_client
