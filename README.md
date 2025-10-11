# LMS Project

Проект — простая **LMS (Learning Management System)** на Django с использованием Django REST Framework (DRF).  
Цель — реализовать backend API для платформы онлайн-обучения, где пользователи могут размещать курсы, уроки и оплачивать их через Stripe.

---

## 📌 Функционал

- Авторизация по email с расширенной моделью пользователя (телефон, город, аватар).  
- CRUD API для:
  - курсов,
  - уроков,
  - платежей.  
- Связь «Курс → Уроки» (один-ко-многим).  
- Оплата курсов через **Stripe Checkout**.  
- Сохранение информации о платежах в БД.  
- REST API (все ответы возвращаются в JSON).  

---

## 🛠 Технологии

- Python 3.13+  
- Django 5.x  
- Django REST Framework  
- Stripe API  
- SQLite (по умолчанию) или PostgreSQL  

---
## 📦 Сервисы
- **Backend (Django + DRF)**
- **PostgreSQL**
- **Redis**
- **Celery**
- **Celery Beat**

---
## 🚀 Установка и запуск (локально)

### ✅ Предварительные требования
- Python 3.11+ / 3.13+
- PostgreSQL (если используете PostgreSQL локально)
- Redis (опционально — для кэша/Celery)
- pip / poetry

### Клонирование репозитория

```bash
git clone https://github.com/yourusername/lms_project.git
cd lms_project
```

### Создание окружения и установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# или если используешь poetry
# poetry install
```

### Создание .env

Скопируй шаблон и отредактируй:

```bash
cp .env.example .env
# затем открой .env и заполни значения
```

### Пример .env (локально)

```dotenv
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=lms_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_pass
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0

STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_PUBLIC_KEY=pk_test_your_public_key
```

### Инициализация базы и миграции

Если используешь PostgreSQL локально — создай БД и пользователя or используй Docker (см. ниже).

Подключись к psql и выполните:

```sql
CREATE USER test_user WITH PASSWORD 'test_pass';
CREATE DATABASE lms_db OWNER test_user;
GRANT ALL PRIVILEGES ON DATABASE lms_db TO test_user;
```

Затем примените миграции и создайте суперпользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Запустите сервер:

```bash
python manage.py runserver
```

Приложение доступно: http://127.0.0.1:8000

---
## 📦 Запуск через Docker / docker-compose

### Пример `docker-compose.yml` (минимум для локальной разработки)

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: lms_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  web:
    build: .
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

volumes:
  db_data:
```

Запуск:

```bash
docker-compose build
docker-compose up -d
```

Проверка логов:

```bash
docker-compose logs -f web
```

---
## 📡 API эндпоинты

Курсы и уроки

- `GET /api/courses/` — список курсов
- `POST /api/courses/` — создать курс
- `GET /api/courses/{id}/` — получить курс
- `PUT /api/courses/{id}/` — обновить курс
- `DELETE /api/courses/{id}/` — удалить курс
- `GET /api/lessons/` — список уроков
- `POST /api/lessons/` — создать урок

Платежи

- `GET /api/payments/` — список платежей
- `POST /api/payments/` — создать платеж (CRUD)
- `POST /api/payments/create-checkout/{course_id}/` — создать Stripe Checkout Session для курса

Авторизация

- `POST /api/token/` — получить JWT токен
- `POST /api/token/refresh/` — обновить токен

---
## 💳 Работа с платежами (Stripe)

1. Создайте курс в админке (http://127.0.0.1:8000/admin/).
2. Получите id курса.
3. Отправьте POST запрос:

```
POST http://127.0.0.1:8000/api/payments/create-checkout/{course_id}/
Authorization: Bearer <your_token>
```

Пример ответа:

```json
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_..."
}
```

Перейдите по `checkout_url`, чтобы оплатить курс.

---
## 🧪 Тесты API (Postman)

В проекте есть Postman-коллекция для тестирования API. В неё включены сценарии:
- создание курса и урока,
- авторизация,
- CRUD платежей,
- создание Stripe Checkout-сессии.

---
## 🌐 Настройка удалённого сервера и деплой (подробно)

Ниже — инструкция для VPS (Ubuntu 22.04) с Docker, nginx и Certbot для HTTPS.

### 1) Подготовка сервера

```bash
# обновляем систему
sudo apt update && sudo apt upgrade -y

# устанавливаем Docker и docker-compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# выйдите и войдите снова, чтобы изменения групп применились

sudo apt install -y docker-compose nginx certbot python3-certbot-nginx
```

### 2) Клонирование репозитория и настройка

```bash
git clone https://github.com/yourusername/lms_project.git
cd lms_project
cp .env.example .env
# отредактируйте .env — укажите реальные ключи и домен
```

### 3) Docker-compose

Соберите и запустите контейнеры:

```bash
docker-compose build
docker-compose up -d
```

Примените миграции и соберите статику (если web контейнер не делает этого автоматически):

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### 4) Настройка nginx (reverse proxy)

Пример конфигурации `/etc/nginx/sites-available/lms`:

```nginx
server {
    listen 80;
    server_name example.com www.example.com; # замените на ваш домен

    location /static/ {
        alias /path/to/your/project/static/; # путь на сервере
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Включите сайт и перезапустите nginx:

```bash
sudo ln -s /etc/nginx/sites-available/lms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5) HTTPS (Certbot)

```bash
sudo certbot --nginx -d example.com -d www.example.com
```

### 6) Автоматический деплой через systemd (опционально)

Создайте unit-файл `/etc/systemd/system/lms.service`:

```ini
[Unit]
Description=Docker Compose LMS
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/lms_project
ExecStart=/usr/bin/docker-compose up -d --build
ExecStop=/usr/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable lms.service
sudo systemctl start lms.service
```

### 7) Логи и отладка

- Просмотр логов контейнера web:

```bash
docker-compose logs -f web
```

- Убедитесь, что переменные в `.env` соответствуют настройкам в `settings.py`.

---
## ⚙️ Настройка CI/CD (GitHub Actions)

### Общая идея
- CI поднимает временный контейнер PostgreSQL и Redis,
- запускает миграции,
- прогоняет тесты.

### Где смотреть workflow
- Перейдите в репозиторий на GitHub → вкладка **Actions** → выберите нужный workflow.
- В логе шага `Apply migrations` вы увидите вывод `python manage.py migrate`.

### Переменные окружения для workflow
Убедитесь, что в workflow установлены переменные окружения (пример):

```yaml
env:
  POSTGRES_DB: test_db
  POSTGRES_USER: test_user
  POSTGRES_PASSWORD: test_pass
  POSTGRES_HOST: 127.0.0.1
  POSTGRES_PORT: 5432
```

Если Django в `settings.py` читает `POSTGRES_DB`/`POSTGRES_USER`/`POSTGRES_PASSWORD`, миграции будут применяться к `test_db` — и ошибка `database "lms_db" does not exist` исчезнет.

### Пример шага деплоя (SSH) — optional

Добавьте секреты в GitHub: `SSH_PRIVATE_KEY`, `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`.

```yaml
- name: Deploy to VPS
  uses: appleboy/ssh-action@v0.1.6
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    script: |
      cd /path/to/lms_project
      git pull origin main
      docker-compose pull
      docker-compose up -d --build
```

---
## 🐛 Трудности и их решения (Troubleshooting)

### Ошибка: `django.db.utils.OperationalError: database "lms_db" does not exist`
**Причина:** CI пытается подключиться к `lms_db`, а в workflow поднята база `test_db` (или база не создана).

**Решение:**
- Либо изменить workflow чтобы создавать `lms_db` (в `services.postgres.env.POSTGRES_DB`),
- либо изменить `settings.py`, чтобы он использовал `POSTGRES_DB` из переменных окружения (рекомендовано).

Пример quick-fix для workflow:

```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_DB: lms_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
```

Или в `settings.py`:

```python
DATABASES['default']['NAME'] = os.getenv('POSTGRES_DB', 'lms_db')
```

### Ошибка: `role "test_user" does not exist` при подключении
Создайте пользователя и дайте права:

```sql
CREATE USER test_user WITH PASSWORD 'test_pass';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO test_user;
```

### Проверка доступности Postgres в workflow
В workflow добавь шаг, который ждёт готовности сервиса:

```bash
until pg_isready -h 127.0.0.1 -p 5432 -U test_user; do
  echo "Waiting for postgres..."
  sleep 2
done
```

---
## 🌍 Адрес развернутого приложения

В README нельзя подставлять адрес без фактического развертывания. После деплоя замените плейсхолдер:

```
https://your-domain-or-ip.example.com
```

и добавьте этот адрес в раздел выше.

---
## 📖 Развитие проекта (идеи)

- Вынести бизнес-логику в сервисы (payments/services.py для Stripe).  
- Добавить разграничение доступа по ролям (студент / преподаватель).  
- Подключить PostgreSQL для продакшн-сборки (вместо SQLite).  
- Автоматизировать деплой через GitHub Actions (ssh / rsync / docker pull).  
- Добавить мониторинг и health-check endpoint.

---

## 📞 Контакты

Если нужно — оставьте контакт и я помогу с настройкой Nginx, systemd unit или добавлением шага деплоя в workflow.

---
