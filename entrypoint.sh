#!/bin/sh

echo "Upgrading the DB..."
python -m flask --app run db upgrade

echo "Collecting Static..."
mkdir -p staticfiles
cp -r static/* staticfiles/

echo "Preparation is Done."
exec "$@"