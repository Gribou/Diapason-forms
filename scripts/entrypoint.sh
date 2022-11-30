#!/bin/bash

gunicorn efneproject.wsgi:application --bind 0.0.0.0:${WEB_PORT:-8000} --access-logfile '-' --error-logfile '-' --log-level 'info' --logger-class efneproject.gunicorn.CustomGunicornLogger
