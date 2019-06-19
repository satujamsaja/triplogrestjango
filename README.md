# triplogrestjango
This is simple project build using Django 2.2 and Django Rest Framework. 
This example will create simple API service and desktop class app using Tkinter as CMS and using
JS framework using react, socket-io and nodejs as frontend to display 'realtime' update from the server without page
reload.

# Screenshot

# Requirements
* Python 3
* Nodejs
* npm/yarn
* Django (https://github.com/django/django) 
* djangorestframework (https://www.django-rest-framework.org/)
* requests (https://pypi.org/project/requests/)

# Install and Run
## Django + djangorestframework
* Create virtual environment
* Clone repo to local development
* Switch to virtual environment (workon <env>)
* Install requirements (pip install -r requirements.txt)
* Migrate database (python manage.py migrations)
* Create superuser (python manage.py createsuperuser)
* Run local webserver (python manage.py runserver)
* Access API root page (http://127.0.0.1/api)
* Access admin page (http://127.0.0.1/admin)

## Triplog App
* Run "python triplogapp.py"
* Login with created admin account

## Server (frontend/server)
* Run "npm install"
* Run "node App.js"

## Client (frontend/client)
* Run "npm install"
* Run "npm start"
