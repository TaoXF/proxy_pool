import redis
import logging; logging.basicConfig(level=logging.INFO)

from .settings import HOST, PORT, PASSWORD


class RedisClient(object):

	def __init__(self):
		if PASSWORD:
			self._db = redis.Redis(host=HOST, port=PORT, password=PASSWORD)
		else:
			self._db = redis.Redis(host=HOST, port=PORT)

	def get_half_proxy(self, count):
		proxy_list = self._db.lrange('proxies', 0, count-1)
		self._db.ltrim('proxies', count, -1)
		return proxy_list

	def put_proxy(self, proxy):
		self._db.rpush("proxies", proxy)

	def len_queue(self):
		return self._db.llen('proxies')

	def flush(self):
		self._db.delete('proxies')

