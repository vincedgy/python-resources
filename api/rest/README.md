# API Rest with fastAPI

with for Queue processing with Redis, Python and docker


This project is very much inspired by this [article](https://medium.com/@mike.p.moritz/using-docker-compose-to-deploy-a-lightweight-python-rest-api-with-a-job-queue-37e6072a209b)



I'll (loosely) present few interesting technologies 


- Python 3.8 with :

  - [fastapi](https://fastapi.tiangolo.com/) for REST API
  - [rq](https://python-rq.org/) for queuing using Redis and workers
  - [uvicorn](https://www.uvicorn.org/) which is a very fast non blocking ASGI HTTP/1 server
  - [Redis](https://redis.io/) for simple Queuing yet string mecanisms
  - [Docker](https://www.docker.com/) leader solution for containers for building Python 3.8 image
  - [docker-compose](https://docs.docker.com/compose/) the docker tool for running a local stack


But also

- [pyenv](https://github.com/pyenv/pyenv) for python management and virtualenv


But also also

- [kompose](https://kompose.io/) for migrating from docker-compose to kubernetes
- [kubernetes](https://kubernetes.io/) running a pod of this project


Wushhhh let's do it 🚀



## Install


Prerequisites (as said before) : 

- Python 3.8, 
- pyenv, 
- pyenv-virtualenv, 
- Docker (wich kubernetes cluster activated), 
- docker-compose

Choose whatever you want to install them depending on your system.


### Install Python 3.8.6 with the help of pyenv

```sh
pyenv install 3.8.6
```


### Create a virtualenv for the project

```sh
pyenv virtualenv 3.8.6 apiproj
```


### Activate the virtualenv for the project

```sh
pyenv activate apiproj
```


## Build docker image

```sh
docker build -t myproj:latest .
```



## Run the project with docker-compose


Run this command in a separated terminal so you can see the worker reacting to messages save within the Redis queue.

```sh
docker-compose
```


Then run this command to listen to Redis events

```sh
redis-cli -p 6389 -d 1 MONITOR
```


Finaly launch a bunch of REST request to the API, which will push you payload into the Queue so that the worker will do what is has to do (which is waiting for 5 seconds)

```sh
curl -v http://localhost:5057/groups/group1 -d '{"owner": "foo", "description": "bar"}'
*   Trying ::1...
* TCP_NODELAY set
* Connected to localhost (::1) port 5057 (#0)
> POST /groups/group1 HTTP/1.1
> Host: localhost:5057
> User-Agent: curl/7.64.1
> Accept: */*
> Content-Length: 38
> Content-Type: application/x-www-form-urlencoded
> 
* upload completely sent off: 38 out of 38 bytes
< HTTP/1.1 201 Created
< date: Sat, 11 Apr 2020 07:37:56 GMT
< server: uvicorn
< content-length: 46
< content-type: application/json
< 
* Connection #0 to host localhost left intact
{"job":"2a575fb6-ac7d-4b8e-b2bc-a32e9533a116"}* Closing connection 0
```


This is what should happen on the server side

```sh
docker-compose up              
WARNING: The Docker Engine you're using is running in swarm mode.

Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.

To deploy your application across the swarm, use `docker stack deploy`.

Creating rest_myproj_redis_1 ... done
Creating rest_myproj_api_1    ... done
Creating rest_myproj_worker_1 ... done
Attaching to rest_myproj_redis_1, rest_myproj_worker_1, rest_myproj_api_1
myproj_redis_1   | 1:C 11 Apr 07:22:53.880 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
myproj_redis_1   | 1:C 11 Apr 07:22:53.880 # Redis version=4.0.6, bits=64, commit=00000000, modified=0, pid=1, just started
myproj_redis_1   | 1:C 11 Apr 07:22:53.880 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
myproj_redis_1   | 1:M 11 Apr 07:22:53.883 * Running mode=standalone, port=6379.
myproj_redis_1   | 1:M 11 Apr 07:22:53.883 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
myproj_redis_1   | 1:M 11 Apr 07:22:53.883 # Server initialized
myproj_redis_1   | 1:M 11 Apr 07:22:53.883 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
myproj_redis_1   | 1:M 11 Apr 07:22:53.886 * DB loaded from disk: 0.003 seconds
myproj_redis_1   | 1:M 11 Apr 07:22:53.886 * Ready to accept connections
myproj_worker_1  | 07:22:54 Worker rq:worker:f3b3578c28af41778c7297bd89346372: started, version 1.3.0
myproj_worker_1  | 07:22:54 *** Listening on my_api_queue...
myproj_worker_1  | 07:22:54 Cleaning registries for queue: my_api_queue
myproj_api_1     | INFO:     Started server process [1]
myproj_api_1     | INFO:     Waiting for application startup.
myproj_api_1     | INFO:     Application startup complete.
myproj_api_1     | INFO:     Uvicorn running on http://0.0.0.0:5057 (Press CTRL+C to quit)
myproj_api_1     | INFO:     172.18.0.1:37268 - "POST /groups/group1 HTTP/1.1" 201 Created
myproj_worker_1  | 07:37:56 my_api_queue: worker.runTask('group1', 'foo', 'bar') (2a575fb6-ac7d-4b8e-b2bc-a32e9533a116)
myproj_worker_1  | 07:38:01 my_api_queue: Job OK (2a575fb6-ac7d-4b8e-b2bc-a32e9533a116)
myproj_worker_1  | 07:38:01 Result is kept for 500 seconds
myproj_worker_1  | 07:38:01 Cleaning registries for queue: my_api_queue
```

Check out also the Redis monitor commands and figure out how 'rq' handles automagicaly the queues, the messages etc.



# The end (for now)