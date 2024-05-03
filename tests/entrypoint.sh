#!/bin/sh

date

action=$1

set -e
export PYTHONPATH="./"
export DJANGO_SETTINGS_MODULE='settings'

if [ `which coverage` ] ; then
    export COVERAGE='coverage run'
else
    export COVERAGE='python'
fi

if [ "$action" = "check_database" ]; then
  if [ "$DATABASE" = "postgres" ]
  then
      echo "Waiting for postgres..."
      while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
      done
      echo "PostgreSQL started"
  fi
elif [ "$action" = "runserver" ]; then
  echo runserver
  python -m django runserver --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
elif [ "$action" = "collectstatic" ]; then
  python -m django collectstatic --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
elif [ "$action" = "test" ]; then
  $COVERAGE -m django test --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
elif [ "$action" = "test_coverage_collect" ]; then
  if [ `which coverage` ] ; then
      coverage combine
      coverage xml
      coverage report
  fi
elif [ "$action" = "check_migrations" ]; then
  python -m django makemigrations --dry-run --noinput --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
elif [ "$action" = "makemigrations" ]; then
  python -m django makemigrations --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
elif [ "$action" = "migrate" ]; then
  python -m django migrate --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
else
  python -m django "$@" --traceback --settings=$DJANGO_SETTINGS_MODULE --verbosity 2 --pythonpath="../"
fi
