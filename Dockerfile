# Dockerfile
FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry и зависимости
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

# Копируем весь проект
COPY . /app/

# Указываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "lms_project.wsgi:application", "--bind", "0.0.0.0:8000"]
