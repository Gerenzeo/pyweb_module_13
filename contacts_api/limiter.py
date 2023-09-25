
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from src.conf.config import settings

async def setup_limiter():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)