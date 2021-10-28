from redis import Redis
import json
import logging

logger = logging.getLogger("uvicorn")

redis = Redis(host="redis", db=0)
logger.info("{}: redis connection.".format(__name__))

class Model():
    DB = "default"

    def __init__(self, redis):
        self.redis = redis

    def getKey(self, table, key):
        return self.DB + "." + table + "." + key

    def set(self, key, value):
        return self.redis.set(key, json.dumps(value))

    def get(self, key):
        data = self.redis.get(key)
        if not data:
            return None

        return json.loads(data)

    def delete(self, key):
        return self.redis.delete(key)


def get_connection():
    return redis
