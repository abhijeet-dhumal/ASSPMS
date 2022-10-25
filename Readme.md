## ASSPMS Backend
## ASSSPMS :- Automatic Securuity Survelliance and Parking Management System
## Development Setup

### Local Setup

- `git clone https://github.com/abhijeet-dhumal/ASSPMS.git`

- `cd duonut-back`

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


## Env file
```
SECRET_KEY = "django-insecure-t_3epnw-h0p@i1ttylhmnn3@#oo1@+t!t7(e#vvespx-s7%*iu"
DEBUG=True
ALLOWED_HOSTS='*'
DEPLOYMENT=False
SITE_URL="http://localhost:8000"

NANONETS_MODEL_ID='<MODEL_ID>'
NANONETS_API_KEY='<API_KEY>'

EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_HOST_USER="<USER_EMAIL>"
EMAIL_HOST_PASSWORD="<USER_HOST_PASSWORD>"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

```

## API Documentation
- `http://127.0.0.1:8000/docs/`