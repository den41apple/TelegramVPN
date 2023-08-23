cd app/frontend

echo "APPLY MIGRATIONS"
python manage.py migrate

echo "RUN APP"
python manage.py runserver 0.0.0.0:8000