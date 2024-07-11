import aioredis
from Backend.backend.database import REDIS_HOST, REDIS_PORT

# redis 의존성 주입을 위한 함수
async def get_redis_connection():
    redis = await aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
    try:
        yield redis
    finally:
        await redis.close()
