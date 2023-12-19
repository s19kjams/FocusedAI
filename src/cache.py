from cachetools import TTLCache

cache = TTLCache(maxsize=1000, ttl=60)

def get_cache(key):
    return cache.get(key)

def set_cache(key, value):
    cache[key] = value

def delete_cache(key):
    if key in cache:
        del cache[key]