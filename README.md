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



