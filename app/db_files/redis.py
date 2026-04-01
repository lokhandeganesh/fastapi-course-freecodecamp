import redis.asyncio as redis
from app.db_files.config import settings
from datetime import datetime, timedelta
import zoneinfo
from typing import Optional

# Define the timezone for consistent 7 AM calculation
IST = zoneinfo.ZoneInfo("Asia/Kolkata")

# Initialize a global variable with type hinting
redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize the Redis connection pool."""
    global redis_client
    # Using the pre-built URL from your config (includes password)
    redis_client = redis.from_url(
        url=settings.redis_url,
        encoding="utf-8",
        decode_responses=settings.redis_decode_response,
        max_connections=20,
        retry_on_timeout=True,
        health_check_interval=30
    )


def get_seconds_until_next_7am() -> int:
    """Calculate the seconds timestamp for the next 7 AM IST."""
    # Use IST to ensure the time is accurate regardless of server location
    now = datetime.now(IST)
    next_7am = now.replace(hour=7, minute=0, second=0, microsecond=0)

    if now >= next_7am:
        next_7am += timedelta(days=1)

    return int((next_7am - now).total_seconds())


async def close_redis():
    """Close the Redis connection pool."""
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_redis() -> Optional[redis.Redis]:
    """Dependency for routers to get the Redis client."""
    global redis_client
    return redis_client
