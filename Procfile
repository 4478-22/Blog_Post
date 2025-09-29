web: gunicorn config.wsgi:application --log-file -
# Run migrations, then daphne
web: python manage.py migrate && daphne -b 0.0.0.0 -p 10000 config.asgi:application
