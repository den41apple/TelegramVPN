cd app

echo "APPLY MIGRATIONS"
alembic upgrade head

echo "RUN APP"
python main.py