#!/bin/bash

celery -A efneproject purge || true # ignore error
celery -A efneproject beat --loglevel=INFO &
celery -A efneproject worker -E --loglevel=INFO -Q ${CELERY_QUEUE:-efne}
