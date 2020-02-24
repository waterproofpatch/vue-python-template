#!/usr/bin/bash

echo "Starting UWSGI..."

source /venv/bin/activate && python -m backend.app --init
source /venv/bin/activate && uwsgi --ini /usr/share/wsgi/wsgi.ini &

echo "Starting NGINX..."
exec nginx -g 'daemon off;'

echo "Done."

