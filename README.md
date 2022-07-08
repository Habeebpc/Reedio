# boilerplate-backend
## _ERP Application Backend_

This is an application build using Python Django and Django REST framework.

## Cloning the Repository and moving to the project level

```sh
git clone git@github.com:RentPe-Technologies/boilerplate-backend.git
cd boilerplate-backend
```

## Installation and Setup

The application requires [Python](https://www.python.org/) v3.6+ to run.
Also supporting dependencies include [RabbitMQ](https://www.rabbitmq.com/)

Install the dependencies and requirements after creating a virtuale enviroment for the project.

```sh
python3 -m venv env
pip install -r requirements.txt
```

Install wkhtmltopdf, RabbitMQ and Redis
```sh
sudo apt install redis
```

Initializing the project
```sh
python manage.py migrate
```

Admin user creation (optional) for accessing the django admin
```sh
python manage.py createsuperuser
```

## Running the project
The app needs to run the Django development server, Celery Worker and Beat services in parallel. Run the following commands in seperate terminals after activating the virtual enviroment in them.
To start the Django development server
```sh
python manage.py runserver
```
To start the Celery worker service
```sh
celery -A boilerplate worker -l info -Q boilerplate
```
To start the Celery beat service
```sh
celery -A boilerplate beat -l info
```

Once the serices are up, you can open the browser and navigate the below links
##### Home:
A basic index page
```sh
http://localhost:8000
```
##### Admin:
The Django admin UI
```sh
http://localhost:8000/api/admin/
```
##### API Documentation:
API Documentation page done using [Swagger](https://drf-yasg.readthedocs.io/en/stable/readme.html)
```sh
http://localhost:8000/api/docs/
```

Once this is done the Application is good to go.
