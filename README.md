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

## 🚀 Установка и запуск

1. Клонируйте репозиторий:

- bash
git clone https://github.com/yourusername/lms_project.git
cd lms_project

## 🚀 Запуск проекта
# Сначала создайте .env файл
cp .env.example .env

# Соберите образы
docker-compose build

# Запустите контейнеры
docker-compose up -d

## 📡 API эндпоинты
Курсы и уроки
GET /api/courses/ — список курсов
POST /api/courses/ — создать курс
GET /api/courses/{id}/ — получить курс
PUT /api/courses/{id}/ — обновить курс
DELETE /api/courses/{id}/ — удалить курс
GET /api/lessons/ — список уроков
POST /api/lessons/ — создать урок
## Платежи
GET /api/payments/ — список платежей
POST /api/payments/ — создать платеж (CRUD)
POST /api/payments/create-checkout/{course_id}/ — создать Stripe Checkout Session для курса
Авторизация
POST /api/token/ — получить JWT токен
POST /api/token/refresh/ — обновить токен
## 💳 Работа с платежами (Stripe)
Создайте курс в админке (http://127.0.0.1:8000/admin/).
Получите id курса.
Отправьте запрос в Postman:
POST http://127.0.0.1:8000/api/payments/create-checkout/{course_id}/
Authorization: Bearer <your_token>
Пример ответа:
{
  "checkout_url": "https://checkout.stripe.com/pay/cs_test_..."
}
Перейдите по checkout_url, чтобы оплатить курс.
## 🧪 Тесты API (Postman)
В проекте есть Postman-коллекция для тестирования API.
В ней проверяются:
создание курса и урока,
авторизация,
CRUD платежей,
создание Stripe Checkout-сессии.

## 🌐 Настройка удаленного сервера и деплой
В README указаны инструкции по настройке удаленного сервера и деплоя.
Описаны шаги для запуска workflow и деплоя приложения:
# Подготовка сервера (Ubuntu / Debian):
- Установить Docker и Docker Compose
- Настроить firewall (ufw) и открыть порты 80, 443
# Копирование репозитория на сервер:
git clone https://github.com/yourusername/lms_project.git
cd lms_project
# Настройка .env на сервере:
cp .env.example .env
Заполнить реальные ключи и настройки.
# Сборка и запуск контейнеров:
docker-compose build
docker-compose up -d
# Настройка reverse proxy (nginx) для работы с HTTPS
# Настройка cron или systemd для автоматического обновления контейнеров при деплое
# Проверка логов:
docker-compose logs -f

## 📖 Развитие проекта
Вынести бизнес-логику в сервисы (payments/services.py для Stripe).
Добавить разграничение доступа по ролям (студент / преподаватель).
Подключить PostgreSQL для продакшн-сборки.
Добавить docker-compose для запуска в контейнере.
