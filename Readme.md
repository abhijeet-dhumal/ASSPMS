## ASSPMS Backend
## ASSSPMS :- Automatic Securuity Survelliance and Parking Management System
## Development Setup

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

- `podman build -t asspms .  `
- `podman run -d -it -p 8000:8000 --name asspms localhost/asspms:latest`
- To add sample data in database storage (admin@gmail.com | Abhijeet) - `podman exec -it asspms python manage.py loaddata dumpdata.json`
- In case want to use your own data (create your own admin user) - `podman exec -it asspms python manage.py createsuperuser`



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