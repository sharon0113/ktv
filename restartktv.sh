#!/bin/sh
kill -9 `ps aux |grep gunicorn |grep -v 'grep'|awk '{print  $2}'`
nohup gunicorn --worker-class=gevent ktvlive.wsgi:application -b 127.0.0.1:8000 &


