def redis_kvstore() -> "RedisKVStore":
    try:
        from redis import Redis

        client = Redis.from_url(url="redis://127.0.0.1:6379")
    except ImportError:
        return RedisKVStore(redis_client=None, redis_url="redis://127.0.0.1:6379")
    return RedisKVStore(redis_client=client)
