from flask_rq2 import RQ  # redis queue
from flask_caching import Cache  # caching

# Redis constants
REDIS_HOST = '192.168.99.100'
REDIS_PORT = '6379'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'


def init_rq(app):
    """
    :param app: flask app
    :return: redis queue handle
    """
    # redis host url
    app.config['RQ_REDIS_URL'] = REDIS_URL
    # redis task queue
    rq = RQ(app)
    return rq


def init_cache(app):
    """
    :param app: flask app
    :return: handle to redis cache
    """
    # redis cache
    cache = Cache(app, config={'CACHE_TYPE': 'redis',
                               'CACHE_KEY_PREFIX': 'prime',
                               'CACHE_REDIS_HOST': REDIS_HOST,
                               'CACHE_REDIS_PORT': REDIS_PORT,
                               'CACHE_REDIS_URL': REDIS_URL
                               })
    return cache
