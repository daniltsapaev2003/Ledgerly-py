# Ledgerly

## О проекте
Ledgerly - платформа для аналитики финансовых результатов публичных компаний
Платформа предоставляет информацию об отчетах,мультипликаторах компаний а так-же стоимость ценных бумаг

## Функции

- Регистрация пользователя и аутентификация
- База данныз акций торгующихся на московской бирже
- Поиск компаний
- Интеграция в Tinkoff API
- Операционные результаты компаний 
- Прогнозы аналитиков 

## Стэк технологий

- Python 3.13
- Django
- Django Templates
- HTMX
- Tailwind CSS
- PostgreSQL
- Django ORM
- T-Invest API
- Httpx
- Uv
- Pytest
- Docker

## Архитектура

```text
T-Invest API
     ↓
T-Invest integration
     ↓
PostgreSQL
     ↓
Django
     ↓
Django Templates + HTMX
     ↓
Browser
```

## Структура проекта

```text
Ledgerly/
├── config/                 # Django конфигурация
├── companies/              # База данных и логика работы с таблицей companies
├   ├── models.py           # Модель таблицы компаний
├   ├── views.py            # Функции Логин-Регистрация
├   └── migrations/         # Миграции
├── ledgerly/               # Логика основной работы(регистрации)
├── tinkoff/                # Интеграция T-Invest API 
├   ├── tinkoff.py          # Функции работы с API
├   └── sync_companies.py   # Функция синхронизации базы с API
├── templates/              # HTML Шаблоны
├── static/                 # Статичные файлы
├── manage.py               # Django утилиты
├── pyproject.toml          # Конфигурация проекта и зависимости
├── uv.lock                 # UV зависимости
└── .env                    # Переменные среды

## Требования

- Python 3.13+
- PostgreSQL 16+
- uv
- Node.js and npm

## Installation

### 1. Скопировать репозиторий

```bash
1) git clone <https://github.com/daniltsapaev2003/Ledgerly-py>
2) cd Ledgerly
3) uv venv
4) uv sync
5) npm install
```

## Конфигурация

Создать `.env` файл:

```env
DB_NAME=ledgerly
DB_USER=ledgerly_user
DB_PASSWORD=ВАШ_ПАРОЛЬ
DB_HOST=localhost
DB_PORT=5432
TINKOFF_TOKEN=ВАШ_ТОКЕН_ТИНЬКОФФ

## БАЗА ДАННЫХ

Ledgerly Использует базу данныз PostgreSQL

### Создание базы данных

Создайте базу данных на основе данных из `.env`.

### Примените миграции

```bash
uv run python manage.py migrate
```

Эта команда создает и обновляет таблицы из базы 

### Синхронизация базы данных компании

Чтобы запустить синхронизацию компаний запустите:

```bash
uv run python tinkoff/sync_companies.py
```

## Запуск проекта 

### Запустите Django сервер разработки

```bash
uv run python manage.py runserver
```

Сайт будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

### Запустите Tailwind CSS

В отдельном терминале:

```bash
npm run dev
```

## Интеграция с T-Invest

Ledgerly использует API T-Invest для получения информации о публичных компаниях.

Интеграция состоит из двух основных компонентов:

- `tinkoff/tinkoff.py` — получает и фильтрует данные о компаниях из API T-Invest.
- `tinkoff/sync_companies.py` — синхронизирует полученные данные с базой данных PostgreSQL.

### Поток данных

```text
T-Invest API
     ↓
tinkoff/tinkoff.py
     ↓
sync_companies.py
     ↓
PostgreSQL

## Интеграция с T-Invest

Ledgerly использует API T-Invest для получения информации о публичных компаниях.

Интеграция состоит из двух основных компонентов:

- `tinkoff/tinkoff.py` — получает и фильтрует данные о компаниях из API T-Invest.
- `tinkoff/sync_companies.py` — синхронизирует полученные данные с базой данных PostgreSQL.

### Поток данных

```text
T-Invest API
     ↓
tinkoff/tinkoff.py
     ↓
sync_companies.py
     ↓
PostgreSQL

## Аутентификация

Ledgerly использует собственную систему аутентификации на основе Django Sessions.

### Регистрация

Пользователь может создать аккаунт, указав:

- Имя
- Фамилию
- Номер телефона
- Email
- Пароль

Пароль сохраняется в базе данных в хешированном виде.

### Вход

При входе пользователь указывает:

- Email
- Пароль

Django проверяет введённый пароль с сохранённым хешем.

При успешной аутентификации в сессии сохраняется идентификатор пользователя:

```text
request.session["session"] = user.id

## Тестирование

Для запуска тестов используется `pytest` и `pytest-django`.

### Запуск тестов

```bash
uv run pytest

## Roadmap

Планируемое развитие Ledgerly:

- Расширение базы публичных компаний
- Страница отдельной компании
- Отображение финансовых показателей
- Анализ финансовой отчётности
- Графики и визуализация финансовых данных
- Фильтрация и сравнение компаний
- Расширение интеграции с T-Invest API
- Расширение тестового покрытия