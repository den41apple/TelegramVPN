# Система управления VPN сервером

## Состоит из:
- VPN на основе [Firezone](https://www.firezone.dev/)
- Телеграм бот
- Лендинг + админка на Django

### Установка зависимостей
```
pip install -r requirements.txt
poetry install
```



## Развертывание:

### 1. Установка Firezone
Для начала необходимо сконфигурировать Firezone [по инструкции](https://www.firezone.dev/docs/deploy)


### 2. Создать `.env` файл с переменными окружения:
#### Telegram бот
```
TG_TOKEN = "..."  # Токен телеграм бота
TG_ADMINS = 123,456  # chat_id администраторов через запятую 

# FIREZONE
FZ_HOST = "https://..."  # Хост установленного ранее Firezone
FZ_TOKEN = "7dF8...."  # Сгенерированный токен
```
##### _Если необходим веб-хук_ 
```
TG_UPDATE_MODE = "webhook"
TG_WEBHOOK_HOST = "https://..."  # Хост с https
TG_APP_PORT = 1234 # Должен быть прокинут в ports у сервиса bot в docker-compose.yaml
```
#### Сайт на django
```
DJ_SECRET_KEY = "django-insecure-d0y..."  # Сгенерированный секретный ключ
DJ_TELEGRAM_BOT_URL = "https://t.me/..."
# url-ы с портом разрешенные для генерации csrf токенов, через запятую
DJ_CSRF_TRUSTED_ORIGINS = http://127.0.0..., 
```


### 3. Варианты запуска
#### Docker:
```
docker compose build
docker compose up -d bot  # Телеграм бот
docker compose up -d site  # Сайт на Django
```

#### Вручную:
##### Применение миграций
```
alembic upgrade head
python frontend/manage.py migrate
```
##### Telegram бот
```
python run_telegram_app.py
```
##### Telegram бот
```
python frontend/manage.py runserver
```
