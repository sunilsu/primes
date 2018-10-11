### Primes - a sample implementation of processing a long running task asynchronously

This is a python project that uses Flask to implement HTTP endpoint to accept client requests. I have used a couple of Flask extension packages, flask-rq2 and flask-caching, to implement a redis backed task queue and cache respectively.

* Flask's built in server is meant for development only as it doesn't scale well for a production environment. There are many options to deploy a Flask application in production. For eg, running this project on a Gunicorn server would be simple,
```
gunicorn rest.app:app
```
I used on a windows machine and have not been able to install gunicorn.

* I have installed a redis docker container for redis services. You can pull an image and run a container as below
```
docker pull redis
docker run --name my-redis -p 6379:6379 -d redis
```

Running on a windows machine, I had to connect to the container at a specific IP provided by my virtual box and I have used that in the code.

* Since this project is about handling long running processes, I have used a task queue to asynchronously handle these tasks outside of the regular HTTP request-response cycles. I have used flask-rq2 package which builds a task queue using Redis backend. The post request is handed off to a task queue and returns a job id for querying the status.
`@rq.job` decorator makes it easy to hand off tasks to this task queue.

* I have used flask-caching package to interface with Redis cache. The post request parameters are used as keys in the cache to keep track of which requests are duplicate.
    * This solution is not ideal for the problem at hand. To get a list of primes, a better solution is to look at the overlapping intervals between the existing keys in cache and the request, and make use of cache for all overlapping intervals. This is complicated and I have not attempted to do it.
    * the keys are created as `primes:start_num:end_num` and checked in cache before dispatching for processing.
    
* I have written a few unit tests for PrimeList class in primes package using pytest.  Writing tests for the Flask app is a little more involved. I have to mock task queues and cache so I can proceed testing some of the functions. I did not have time for this.

* In production, I will probably use Java or Go rather than python for this service. I have used Java and Go in the past for rest services, but have been doing python mostly recently and hence the choice.

### Running the project
This should be packaged better with bash scripts to run different parts, but I havent had time,
* Conda environment file fe_env.yml should be used to install all the packages used.

* Download the repo from github and within the root folder of this repo,

```
# Run redis docker container as mentioned above in a terminal
docker run --name my-redis -p 6379:6379 -d redis

# Start the flask app as below in a terminal
export FLASK_APP=rest/app.py
flask run

# You will see the output below,
 * Serving Flask app "rest.app"
 * Forcing debug mode off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

# start redis task queue worker in another terminal
export FLASK_APP=rest/app.py
flask rq worker

# you will see the following (or similar)
11:55:02 RQ worker 'rq:worker:Laptop-Sunil.3081' started, version 0.12.0
11:55:02 *** Listening on default...
11:55:02 Cleaning registries for queue: default

# Now send requests to the server with CURL

curl -i -X POST 'localhost:5000/primes?start_num=4&end_num=11'

# Response with status 200 and UUID below
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Thu, 11 Oct 2018 16:58:05 GMT

"a978649a-99c2-4f45-b927-3658678fd504"

# Now query the status of the task

curl -i -X GET 'localhost:5000/result/a978649a-99c2-4f45-b927-3658678fd504'

# Response below with status 200 and result
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 13
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Thu, 11 Oct 2018 17:00:12 GMT

"[5, 7, 11]"

# Sending the same request return the same id. This is a cache hit and avoids duplicating processing
curl -i -X POST 'localhost:5000/primes?start_num=4&end_num=11'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Thu, 11 Oct 2018 17:02:03 GMT

"a978649a-99c2-4f45-b927-3658678fd504"

# Now starting a long running job, primes less than 1000000
$ curl -i -X POST 'localhost:5000/primes?start_num=1&end_num=1000000'
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Thu, 11 Oct 2018 17:04:00 GMT

"e3aa241f-6ce6-4d19-961e-ae3525620b2a"

# Response with status code 204, still processing
curl -i -X GET 'localhost:5000/result/e3aa241f-6ce6-4d19-961e-ae3525620b2a'
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 3
Server: Werkzeug/0.14.1 Python/3.7.0
Date: Thu, 11 Oct 2018 17:04:33 GMT

```




