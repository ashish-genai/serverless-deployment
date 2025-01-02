from typing import Any, Optional
import redis
from functools import wraps
import json
import os
from datetime import timedelta

# Initialize Redis client
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def cache_key(*args, **kwargs):
    """Generate a cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)

def cache(ttl: int = 300):
    """Cache decorator that stores results in Redis"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = redis_client.get(key)
            if cached_result:
                return json.loads(cached_result)
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(
                name=key,
                time=ttl,
                value=json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern: str):
    """Invalid all cache keys matching the pattern"""
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)

class CacheManager:
    @staticmethod
    def get(key: str) -> Optional[str]:
        return redis_client.get(key)
    
    @staticmethod
    def set(key: str, value: Any, ttl: Optional[int] = None):
        if ttl:
            redis_client.setex(key, ttl, json.dumps(value))
        else:
            redis_client.set(key, json.dumps(value))
    
    @staticmethod
    def delete(key: str):
        redis_client.delete(key)
    
    @staticmethod
    def clear_pattern(pattern: str):
        invalidate_cache(pattern)