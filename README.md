# flask-complex-sample
A complex Flask sample application that run asynchronous jobs using multithread and report some metrics.

[![Docker Build Statu](https://img.shields.io/docker/build/mtulio/flask_sample.svg)](https://hub.docker.com/r/mtulio/flask_sample/)

## Overview

This project is more an study case using Flask framework, now I'm approaching some concepts:
* Future
* Queues
* Multithread
* Metrics*
* Metrics report to Librato*
* Metrics report to Zabbix*

### Metrics (TODO)

* Keep internal metrics of all of the queues
* Keep Flask metric
* Report custom metrics to Librato
* Report custom metrics to Zabbix

## USAGE

* Install the dependencies

`make setup`

* Run the application localy

`make run`

* Run in docker
 * Build
 * Run

1)

`make docker-build`

2)

```bash
$ make docker-run
sudo docker run --rm -p 5000:5000 --name flask_app -d flask_app:0.2.0
c573c441dfe36c19ffc1d8c2c165bb1c9a571f9628ee9c6ed6b91dd0777af062
sleep 2 && curl http://localhost:5000/status
{
  "pool": {
    "_finished": {
      "_count": 0,
      "_max": 100
    },
    "_running": {
      "_count": 0,
      "_max": 5
    },
    "_waiting": {
      "_count": 0,
      "_max": 100
    },
    "manager": "<Future at 0x7f1b38260a90 state=running>"
  },
  "this": "<Request 'http://localhost:5000/status' [GET]>",
  "version": "0.2.0"
}

```

* Simple status - only counters and sys info

```bash
$ http http://localhost:5000/status
HTTP/1.0 200 OK

{
    "pool": {
        "_finished": {
            "_count": 50,
            "_max": 100
        },
        "_running": {
            "_count": 0,
            "_max": 5
        },
        "_waiting": {
            "_count": 0,
            "_max": 100
        },
        "manager": "<Future at 0x7f7f598db160 state=running>"
    },
    "this": "<Request 'http://localhost:5000/status' [GET]>",
    "version": "0.1.0"
}
```

* run the sample job

```
$ http http://localhost:5000/run
HTTP/1.0 200 OK

Two jobs was launched in background!

```

* Detailed the thread status

```
http http://localhost:5000/status/details
HTTP/1.0 200 OK

{
   "pool": {
       "_finished": {
           "_count": 1,
           "_max": 100,
           "list": [
               {
                   "_args": "{'a2': 123, 'func': <bound method Tasks.run_sleep30 of <app.tasks.Tasks object at 0x7fecaaabb630>>, 'a1': 'aaa', 'alias': 'task2'}",
                   "_func": "<bound method Tasks.run_sleep30 of <app.tasks.Tasks object at 0x7fecaaabb630>>",
                   "_result": "True",
                   "_time": "1505690055.8564484",
                   "job": "<Future at 0x7fecaaa65da0 state=finished returned bool>",
                   "name": "task2"
               }
           ]
       },
       "_running": {
           "_count": 1,
           "_max": 5,
           "list": [
               {
                   "_args": "{'func': <bound method Tasks.run_sleep15 of <app.tasks.Tasks object at 0x7fecaaabb630>>, 'alias': 'task1'}",
                   "_func": "<bound method Tasks.run_sleep15 of <app.tasks.Tasks object at 0x7fecaaabb630>>",
                   "job": "<Future at 0x7fecaaa65b00 state=running>",
                   "name": "task1"
               }
           ]
       },
       "_waiting": {
           "_count": 0,
           "_max": 100
       },
       "manager": "<Future at 0x7fecaab28a90 state=running>"
   },
   "this": "<Request 'http://localhost:5000/status/details' [GET]>",
   "version": "0.2.0"
}

```

* run 19 sample jobs - each run will schedulle 2 jobs, so 38 jobs will be schedulled

```bash
for X in $(seq 1 19); do http http://localhost:5000/run; done
```

* kill and remove the container

`make docker-kill`


## TODO

* Unit tests
* Converage tests
