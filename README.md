# flask-complex-sample
A complex Flask sample application that run asynchronous jobs using multithread and report some metrics.

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

### Check status

* Simple status - only counters and sys info

* Detailed thread status

```bash
$ http http://localhost:5000/status
HTTP/1.0 200 OK
Content-Length: 354
Content-Type: application/json
Date: Sun, 17 Sep 2017 22:30:08 GMT
Server: Werkzeug/0.12.2 Python/3.5.2

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

### Run sample jobs

* run 19 jobs

```bash
for X in $(seq 1 19); do http http://localhost:5000/run; done
```

* check the status

```bash
$ http http://localhost:5000/status
HTTP/1.0 200 OK
Content-Length: 355
Content-Type: application/json
Date: Sun, 17 Sep 2017 22:24:12 GMT
Server: Werkzeug/0.12.2 Python/3.5.2

{
    "pool": {
        "_finished": {
            "_count": 26,
            "_max": 100
        },
        "_running": {
            "_count": 5,
            "_max": 5
        },
        "_waiting": {
            "_count": 19,
            "_max": 100
        },
        "manager": "<Future at 0x7f7f598db160 state=running>"
    },
    "this": "<Request 'http://localhost:5000/status' [GET]>",
    "version": "0.1.0"
}
```


## TODO

* Unit tests
* Converage tests
