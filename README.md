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

Створіть файл налаштувань:

bashcp .env.example .env
# Відредагуйте .env файл

Запустіть контейнери:

bashdocker-compose up -d --build

Система буде доступна за адресами:


Web: http://localhost
API: http://localhost/api/
Admin: http://localhost/admin/
Flower: http://localhost:5555

Локальне встановлення

Створіть віртуальне середовище:

bashpython -m venv venv
source venv/bin/activate  # Linux/Mac

Встановіть залежності:

bashpip install -r requirements.txt

Налаштуйте базу даних:

bashcreatedb booking_db
python manage.py migrate
python manage.py createsuperuser

Запустіть сервери:

bash# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery Worker
celery -A booking_project worker -l info

# Terminal 3: Celery Beat
celery -A booking_project beat -l info

# Terminal 4: FastAPI
cd fastapi_app
uvicorn main:app --reload --port 8001
Структура проекту
booking-system/
├── booking/              # Django додаток
├── booking_project/      # Django налаштування
├── fastapi_app/         # FastAPI мікросервіс
├── static/              # Статичні файли
├── media/               # Завантажені файли
├── docker-compose.yml   # Docker конфігурація
└── requirements.txt     # Python залежності
API Документація
FastAPI автоматично генерує документацію:

Swagger UI: http://localhost:8001/docs
ReDoc: http://localhost:8001/redoc

Тестування
bash# Django тести
python manage.py test

# Coverage
coverage run --source='.' manage.py test
coverage report
Розгортання на продакшн

Оновіть .env файл для продакшн
Використовуйте docker-compose.prod.yml
Налаштуйте SSL сертифікати
Налаштуйте backup бази даних

Ліцензія
MIT License
Підтримка
Для питань та пропозицій створюйте Issue в репозиторії.

## Крок 10: Фінальні кроки для запуску

### 10.1. Створення всіх файлів та директорій

```bash
# Створити всю структуру
mkdir -p booking-system
cd booking-system

# Ініціалізація git
git init

# Створити всі директорії
mkdir -p booking/{templates/booking/{partials,emails},migrations}
mkdir -p booking_project
mkdir -p fastapi_app/routers
mkdir -p static media templates

# Створити порожні __init__.py файли
touch booking/__init__.py
touch booking/migrations/__init__.py
touch booking_project/__init__.py
touch fastapi_app/__init__.py
touch fastapi_app/routers/__init__.py

# Створити всі файли згідно структури вище
10.2. Перевірка перед запуском
bash# Перевірити структуру
tree -L 3

# Перевірити Docker
docker --version
docker-compose --version

# Перевірити Python
python --version
10.3. Запуск системи
bash# Спосіб 1: Docker (рекомендовано)
docker-compose up -d --build

# Перевірити статус
docker-compose ps

# Переглянути логи
docker-compose logs -f

# Спосіб 2: Локально
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
10.4. Перші кроки після запуску

Відкрийте http://localhost/admin/
Увійдіть як admin/adminpassword
Створіть тестовий календар
Створіть тестову подію
Перевірте роботу нагадувань

Усунення проблем
Проблема з PostgreSQL
bash# Перевірити з'єднання
docker-compose exec postgres psql -U booking_user -d booking_db

# Перезапустити
docker-compose restart postgres
Проблема з міграціями
bash# Видалити міграції та створити заново
rm -rf booking/migrations/
python manage.py makemigrations booking
python manage.py migrate
Проблема зі статичними файлами
bashpython manage.py collectstatic --clear --noinput
