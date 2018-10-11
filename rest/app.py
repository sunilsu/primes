"""
This exposes http endpoint for the client.
Redis is used as backend for task queue and caching,
using flask extensions for them
"""
from flask import Flask, request, jsonify
from flask_rq2 import RQ  # redis queue
from flask_caching import Cache # caching
from rq.job import Job
from primes.primes import PrimesList
from rest.invalid import InvalidUsage

# url parameter names
START_NUM = 'start_num'
END_NUM = 'end_num'

# Redis constants
REDIS_HOST = '192.168.99.100'
REDIS_PORT = '6379'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'


# Flask app
app = Flask('Prime')
# redis host url
app.config['RQ_REDIS_URL'] = REDIS_URL
# redis task queue
rq = RQ(app)
# redis cache
cache = Cache(app, config={'CACHE_TYPE': 'redis',
                           'CACHE_KEY_PREFIX': 'prime',
                           'CACHE_REDIS_HOST': REDIS_HOST,
                           'CACHE_REDIS_PORT': REDIS_PORT,
                           'CACHE_REDIS_URL': REDIS_URL
                           })


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """
    :param error: a InvalidUsage instance
    :return: Response object with error msg and status code
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def validate_request(args):
    """
    :param args: api request params, a dictionary
    :return: (start_num, end_num) tuple, raises InvalidUsage if validation fails
    """
    msg = []
    if START_NUM not in args:
        msg.append(f'Missing {START_NUM}')
    if END_NUM not in args:
        msg.append(f'Missing {END_NUM}')
    if msg:
        raise InvalidUsage('\n'.join(msg))
    start_num = int(args[START_NUM])
    end_num = int(args[END_NUM])

    if start_num < 0 or end_num < 0:
        raise InvalidUsage(f'{START_NUM} and {END_NUM} cannot be negative')

    if end_num <= start_num:
        raise InvalidUsage(f'{END_NUM} has to be greater than {START_NUM}')
    return start_num, end_num


@rq.job
def get_primes_list(start, end):
    """
    This is a redis queue task
    :param start: int, start of range for primes list
    :param end: int, end of range for primes list
    :return: primes in the range [start_num, end_num]
    """
    primes_list_obj = PrimesList(start, end)
    primes_list = primes_list_obj.primes_list()
    return primes_list


@app.route('/primes', methods=['POST'])
def primes():
    """
    method to handle primes list request which has a start_num and end_num
    checks cache for previously submitted job for this range and returns the job id from cache
    :return: job_id (uuid) and HTTP status code (200) if request is valid
             else returns a 400 status code with error message
    """
    try:
        args = request.args
        start_num, end_num = validate_request(args)
        # cache key
        key = f'primes:{start_num}:{end_num}'
        rv = cache.get(key)
        if rv is None: # not in cache
            job = get_primes_list.queue(start_num, end_num)
            print(job.get_id())
            cache.set(key, job.get_id(), timeout=3600)
            return jsonify(job.get_id()), 200
        else:
            return jsonify(rv), 200
    except Exception as e:
        raise InvalidUsage("Error Processing request {}".format(e))


@app.route('/result/<uuid:job_id>')
def task_result(job_id):
    """
    :param job_id: UUID for a primes list task submitted previously
    :return: the job result if completed or HTTP status 204 if not
    """
    try:
        job = Job.fetch(str(job_id), connection=rq.connection)
        if job.is_finished:
            return jsonify(str(job.result)), 200
        else:
            return jsonify(), 204
    except Exception as e:
        raise InvalidUsage("Error Processing request {}".format(e))
