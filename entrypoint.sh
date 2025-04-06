#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
#exec gunicorn enrollverse_be.wsgi:application --bind 0.0.0.0:8000
exec python manage.py runserver 0.0.0.0:8000
