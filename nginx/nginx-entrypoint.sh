#!/bin/sh

mkdir -p /var/log/nginx

exec nginx -g "daemon off;"