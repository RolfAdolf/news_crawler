#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $DB_HOST $DB_PORT; do
      echo "Waiting for PostgreSQL to complete initialization at $DB_HOST:$DB_PORT..."
      sleep 5
    done

    echo "News Crawler has been started!"
fi

exec "$@"