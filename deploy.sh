#!/bin/sh     
sudo git pull
/home/ubuntu/boilerplate-backend/envs/bin/python3.8 manage.py makemigrations
/home/ubuntu/boilerplate-backend/envs/bin/python3.8 manage.py migrate
sudo supervisorctl restart boilerplate_api boilerplate_celery boilerplate_beat