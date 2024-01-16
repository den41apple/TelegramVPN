# Система управления VPN сервером

## Состоит из:
- VPN на основе [Firezone](https://www.firezone.dev/)
- Телеграм бот

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
```ini
TG_TOKEN = "..."  # Токен телеграм бота
TG_ADMINS = 123,456  # chat_id администраторов через запятую 

# FIREZONE
FZ_HOST = "https://..."  # Хост установленного ранее Firezone
FZ_TOKEN = "7dF8...."  # Сгенерированный токен
```
##### _Если необходим веб-хук_ 
```ini
TG_UPDATE_MODE = "webhook"
TG_WEBHOOK_HOST = "https://..."  # Хост с https
TG_APP_PORT = 1234 # Должен быть прокинут в ports у сервиса bot в docker-compose.yaml
```


### 3. Варианты запуска
#### Docker:
```shell
docker compose build
docker compose up -d bot  # Телеграм бот
```

#### Вручную:
##### Применение миграций
```shell
alembic upgrade head
python frontend/manage.py migrate
```
##### Telegram бот
```shell
python run_app.py
```

