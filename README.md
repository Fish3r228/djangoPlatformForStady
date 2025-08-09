# LMS Project

Проект — простая LMS (Learning Management System) на Django с использованием Django REST Framework (DRF).  
Цель — реализовать backend API для платформы онлайн-обучения, где пользователи могут размещать курсы и уроки.

---

## Описание проекта

- Авторизация по email с расширенной моделью пользователя (телефон, город, аватарка).  
- CRUD API для курсов и уроков.  
- Курсы содержат множество уроков (связь один-ко-многим).  
- Проект построен как REST API, возвращает JSON.  
- Пока без авторизации и ограничений доступа.

---

## Технологии

- Python 3.9+  
- Django 4.x  
- Django REST Framework  
- SQLite (по умолчанию, можно сменить на PostgreSQL)  

---

## Установка и запуск

1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/lms_project.git
cd lms_project

