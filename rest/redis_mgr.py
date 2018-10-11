from flask_rq2 import RQ  # redis queue
from flask_caching import Cache # caching

# Redis constants
REDIS_HOST = '192.168.99.100'
REDIS_PORT = '6379'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'