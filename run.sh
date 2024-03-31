#!/bin/sh

python manage.py makemigrations
python manage.py migrate --no-input

#create default admin user
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model();  CustomUser.objects.create_superuser('admin@gmail.com', 'admin_password')" | python manage.py shell
#create default simple user
echo "from django.contrib.auth import get_user_model; CustomUser = get_user_model();  CustomUser.objects.create_user('simple_user@gmail.com', 'simple_user_password')" | python manage.py shell

gunicorn app.wsgi:application --bind 0.0.0.0:8000 &

unlink /etc/nginx/sites-enabled/default
nginx -g 'daemon off;'
