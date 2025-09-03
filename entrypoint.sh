#!/bin/sh

echo "Upgrading the DB..."
python -m flask --app run db upgrade

exec "$@"