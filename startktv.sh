#!/usr/bin/sh

nohup gunicorn --worker-class=gevent ktvlive.wsgi:application -b 127.0.0.1:8000 &


