web: gunicorn mysite.wsgi
release:
  python manage.py collectstatic --noinput
  python manage.py makemigrations
  python manage.py makemigrations housing 
  python manage.py migrate --run-syncdb
