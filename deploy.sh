#!/bin/sh     
sudo git pull
/home/ubuntu/tech_plotz-backend/envs/bin/python3.8 manage.py makemigrations
/home/ubuntu/tech_plotz-backend/envs/bin/python3.8 manage.py migrate
sudo supervisorctl restart tech_plotz_api tech_plotz_celery tech_plotz_beat