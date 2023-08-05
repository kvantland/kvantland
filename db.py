import psycopg
from psycopg.types.composite import CompositeInfo, register_composite
import bottle
import inspect

register_composite(CompositeInfo('point', 600, 1017, field_names=('x', 'y'), field_types=(701, 701)))

class PostgresPlugin(object):
	name = 'postgres'
	api = 2

	def __init__(self, url: str, keyword='db'):
		self.url = url
		self.keyword = keyword

	def setup(self, app):
		self.connection = psycopg.connect(self.url)

	def apply(self, callback, route):
		config = route.config
		_callback = route.callback

		config_get = lambda key, default: config.get('postgres.' + key, default)

		url = config_get('url', self.url)
		keyword = config_get('keyword', self.keyword)

		if keyword not in inspect.signature(_callback).parameters:
			return callback

		def wrapper(*args, **kwargs):
			with self.connection.transaction():
				with self.connection.cursor() as cur:
					kwargs[keyword] = cur
					yield from callback(*args, **kwargs)

		return wrapper

Plugin = PostgresPlugin
