#!/usr/bin/env bash
set -e

# wait for dependent services
if [ "$WAIT_FOR_DB" = "true" ]; then
  echo "Waiting for database..."
  until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
  done
fi

# run migrations and collectstatic if asked
if [ "$DJANGO_MIGRATE" = "true" ]; then
  python manage.py migrate --noinput
fi

if [ "$DJANGO_COLLECTSTATIC" = "true" ]; then
  python manage.py collectstatic --noinput
fi

# start gunicorn
exec gunicorn DjangoPlatformForStady.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS:-3} \
    --access-logfile '-' \
    --error-logfile '-'
