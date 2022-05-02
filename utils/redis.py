import redis
from django.conf import settings


def get_redis():
    return redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
