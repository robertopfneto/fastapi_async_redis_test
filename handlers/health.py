import asyncio

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from modules.health import check_postgres, check_redis

router = APIRouter()

@router.get("/ping")
async def ping():
    redis_ok, postgres_ok = await asyncio.gather(check_redis(), check_postgres())
    healthy = redis_ok and postgres_ok
    
    message = "pong :)" if healthy else "not pong :("
    status_code = 200 if healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "message": message,
            "is_redis_connected": str(redis_ok),
            "is_postgres_connected": str(postgres_ok)
        }
    )
