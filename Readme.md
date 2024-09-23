## ASSSPMS :- IOT based Automatic Security Surveillance and Parking Management System
- This Application is built with Django and Rest API framework which enables Hardware (Camera Sensor and Microcontroller) to interact with webserver using REST API protocol
- Purpose : To build an automated application which can be used to monitor and manage Security Surveillance and Parking Management by reducing relative human efforts required by great margin.
- [Published Journal](https://www.ijera.com/papers/vol13no4/1304171177.pdf)

### Local Setup

- `git clone https://github.com/abhijeet-dhumal/ASSPMS.git`

- `cd ASSPMS`

## Without using Container

- Create Virtual Environment `virtualenv venv`

- Activate Virtual Environment 
    - Windows - `venv/Scripts/activate.ps1`
    - Linux - `source venv/bin/activate`

- Install Dependencies `pip install -r requirements.txt`

- Add `.env` file

- Run Migratations `python manage.py migrate`

- Create Super User `python manage.py createsuperuser`
    - Enter Username and Password and Create Super User

- Start Server `python manage.py runserver`

## Using container

- `podman build -t asspms .` # to build Custom container-image using Dockerfile
- `podman run -d -it -p 8000:8000 --name asspms localhost/asspms:latest` # to run custom container-image
- To run application, just install Container engine (Docker/Podman) on your local system and run below command : 

`podman run --rm -d -it -p 8000:8000 --name asspms quay.io/abdhumal/asspms:0.0.1`

or

`podman run --rm -d -it -p 8000:8000 --name asspms docker.io/abhijeetdhumal0798/asspms:0.0.2`



## Env file
```
SECRET_KEY = "django-insecure-t_3epnw-h0p@i1ttylhmnn3@#oo1@+t!t7(e#vvespx-s7%*iu"
DEBUG=True
ALLOWED_HOSTS='*'
DEPLOYMENT=False
SITE_URL="http://localhost:8000"

DJANGO_SETTINGS_MODULE = "app.settings"
DJANGO_SUPERUSER_PASSWORD="<admin-password>"
DJANGO_SUPERUSER_EMAIL="admin@gmail.com"
DJANGO_SUPERUSER_USERNAME="admin"
DB_NAME="db.sqlite3"

 
#-----  add below variables in case of hosted DB  ----------
#Reference blog : https://medium.com/@stevelukis/connecting-django-to-amazon-rds-c563bad0483e
# DB_HOSTNAME=""
# DB_PORT=""
# DB_USERNAME=""
# DB_PASSWORD=""


#----- to specify model data for OCR based model ------
# Reference GitHub : https://github.com/NanoNets/nanonets-ocr-sample-python

NANONETS_MODEL_ID='<MODEL_ID>'
NANONETS_API_KEY='<API_KEY>'


#------ to add email creds -------------
# Reference blog : https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab

#In case of printing email data on localhost terminal console
#EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="<USER_EMAIL>"
EMAIL_HOST_PASSWORD="<USER_HOST_PASSWORD>"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

## API Documentation
- `http://127.0.0.1:8000/docs/`

## Public API reference used for OCR 
- `https://github.com/NanoNets/nanonets-ocr-sample-python`

## Default Credentials
Admin credentials (email/password) : `admin@gmail.com` / `Abhijeet`

Simple user Credentials : `user1@gmail.com` / `Abhijeet`
