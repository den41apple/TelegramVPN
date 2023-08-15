cd app

echo "APPLY MIGRATIONS"
alembic upgrade head

echo "RUN APP"
python run_telegram_app.py