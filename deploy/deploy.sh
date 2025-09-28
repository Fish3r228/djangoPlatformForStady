#!/usr/bin/env bash
set -e

# Путь к проекту на сервере
PROJECT_DIR=/srv/myproject

# Переключаемся в директорию
cd $PROJECT_DIR

# Обновляем код
git fetch --all
git reset --hard origin/${CI_BRANCH:-main}

# Скачиваем образы или пересобираем
docker compose pull || true
docker compose build --no-cache

# Запускаем с пересборкой поднимаем сервисы
docker compose up -d --remove-orphans

# Очистка старых образов
docker image prune -f
