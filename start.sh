#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn settings.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 3