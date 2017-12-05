#!/bin/bash

if [[ ! -d "logs/" ]]; then
    echo "Creating logs folder"
    mkdir logs
fi

if [[ $1 = "serv" ]]; then
    if [[ -z $2 ]]; then
        port=8080
    else
        port=$2
    fi
    echo "Run server on $port"
    find . -name \*.pyc -delete
    python manage.py runserver "0:$port"
elif [[ $1 = "updb" ]]; then
    echo "Updating database"
    python manage.py makemigrations
    python manage.py migrate
elif [[ $1 = "test" ]]; then
    echo "Run tests"
    python manage.py test
elif [[ $1 = "env" ]]; then
    echo "Add environment variables"
    # gen key
    export LIT_NOTHING_TO_SEE_HERE=$(python -c 'import random; print("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]))')
    export TEST_ENV=1
elif [[ $1 = "cadmin" ]]; then
    python manage.py createsuperuser
else
    echo "Try again"
fi
