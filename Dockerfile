FROM python:3.10.12-slim-bookworm

RUN pip install --upgrade pip "poetry==1.5.1"
RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-ansi --only main

CMD ["python", "app/run_telegram_app.py"]