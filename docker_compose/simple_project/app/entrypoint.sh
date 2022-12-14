#!/usr/bin/env bash

set -e
chown www-data:www-data /var/log

export $(xargs < .env)

until PGPASSWORD="$PASSWORD" psql -h "$HOST" -d "$NAME" -U "$USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

python3 manage.py makemessages -l en -l ru
python3 manage.py collectstatic --noinput
python3 manage.py migrate --fake-initial
uwsgi --strict --ini /opt/app/uwsgi/uwsgi.ini