#!/usr/bin/env bash
set -e

# Default to production-friendly settings if not supplied
export DJANGO_DEBUG=${DJANGO_DEBUG:-False}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-config.settings}

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting: $@"
exec "$@"
