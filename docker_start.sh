#!/usr/bin/bash

# Init the database with test data
echo "Init database..."
source /venv/bin/activate && python -m backend.app --init --testdata

# Start the WSGI server so the Flask app can receive requests from NGIN
echo "Starting UWSGI..."
source /venv/bin/activate && uwsgi --ini /usr/share/wsgi/wsgi.ini &

# Start the NGINX (daemon off so docker container doesn't exit)
echo "Starting NGINX..."
exec nginx -g 'daemon off;'

