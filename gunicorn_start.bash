#!/bin/bash

NAME="super_detector"                                   # Name of the application
DJANGODIR=/home/ubuntu/fake-product-detector               # Django project directory
SOCKFILE=/home/ubuntu/django_env/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                         # the user to run as
GROUP=ubuntu                                        # the group to run as
NUM_WORKERS=1                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=detector.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=detector.wsgi              # WSGI module name
ACCESS_LOGFILE=/home/ubuntu/logs/gunicorn-access.log
ERROR_LOGFILE=/home/ubuntu/logs/gunicorn-error.log
LOG_LEVEL=info 
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
source /home/ubuntu/django_env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
echo "starting virtaul env"

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=$LOG_LEVEL \
  --access-logfile=$ACCESS_LOGFILE \
  --error-logfile=$ERROR_LOGFILE
  #--log-file=$LOG_FILE
