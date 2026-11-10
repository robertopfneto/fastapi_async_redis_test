import asyncio # async padrao do yton
import os

import asyncpg 
from redis.asyncio import Redis
from redis.exceptions import RedisError

async def check_redis() -> bool:
    url = os.getenv("REDIS_URL")
    if not url:
        return False

    try:
        async with Redis.from_url(url) as client:
            return await asyncio.wait_for(client.ping(), timeout=3)
        
    except (RedisError, OSError, asyncio.TimeoutError, ValueError):
        return False



async def check_postgres() -> bool:
    url = os.getenv("DATABASE_URL")
    if not url:
        return False

    try:
        connection = await asyncpg.connect(
            url, ssl="require", timeout=3, command_timeout=3
        )
        try:
            return await connection.fetchval("SELECT 1") == 1
        finally:
            await connection.close(timeout=3)
    except (
        asyncpg.PostgresError,
        asyncpg.InterfaceError,
        OSError,
        asyncio.TimeoutError,
        ValueError,
    ):
        return False