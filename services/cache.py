from redis import asyncio as aioredis
import os
import json
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")  # Загружаем из .env

redis = None  # Глобальная переменная для подключения

async def init_redis():
    """Инициализирует подключение к Redis."""
    global redis
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)

async def get_cached_response(cache_key: str):
    """Пытается получить закэшированный ответ по ключу."""
    if redis is None:
        await init_redis()
    
    print(f"[КЭШ] Проверяем ключ: {cache_key}")  # Логируем ключ
    
    cached_data = await redis.get(cache_key)
    if cached_data:
        print("[КЭШ] Найдено в кэше ✅")
        return json.loads(cached_data)
    
    print("[КЭШ] Нет в кэше ❌")
    return None


async def cache_response(cache_key: str, response: str, ttl: int = 3600):
    """Кэширует ответ на определённое время (TTL в секундах)."""
    if redis is None:
        await init_redis()
    
    await redis.set(cache_key, json.dumps(response), ex=ttl)
