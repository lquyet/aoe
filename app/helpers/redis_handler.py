import redis
from app.config import settings


class RedisHandler:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not RedisHandler.__instance:
            RedisHandler.__instance = RedisHandler()
        return RedisHandler.__instance

    def __init__(self):
        self.redis_host = settings.REDIS_HOST
        self.redis_port = settings.REDIS_PORT
        self.redis_db = settings.REDIS_DB
        self.redis_password = settings.REDIS_PASSWORD
        self.client = redis.Redis(
            host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_password)

    def insert_redis(self, data: dict):
        try:
            self.client.mset(data)
            return True
        except Exception as e:
            raise Exception(f'Insert Redis error: {e}')

    def get_object(self, element: str):
        return self.client.get(element)


redis_handler = RedisHandler()
