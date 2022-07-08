FROM python:3

ENV PYTHONUNBUFFERD=1

WORKDIR /srv/boilerplate/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
