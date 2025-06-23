# Booking System - Система бронювання зустрічей

Веб-додаток для планування зустрічей та управління розкладом з підтримкою календарів, нагадувань та real-time оновлень.

## Функціональність

- 📅 Створення та управління календарями
- 📧 Email/SMS нагадування
- 🔍 Пошук вільних часових слотів
- 👥 Управління учасниками подій
- 🔐 Гнучка система прав доступу
- 📊 Статистика та звіти
- 🔄 Real-time оновлення через WebSocket
- 📱 Адаптивний дизайн

## Технології

- **Backend**: Django 5.0, FastAPI
- **Frontend**: HTML, Tailwind CSS, HTMX, Alpine.js, FullCalendar.js
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Task Queue**: Celery
- **Web Server**: Nginx, Gunicorn, Uvicorn
- **Container**: Docker, Docker Compose

## Швидкий старт

### Вимоги

- Python 3.11+
- Docker і Docker Compose
- PostgreSQL 15+
- Redis 7+

### Встановлення через Docker

1. Клонуйте репозиторій:
```bash
git clone <repository-url>
cd booking-system
