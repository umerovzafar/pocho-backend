# Тестирование

## Запуск тестов

### Установка зависимостей для тестирования

```bash
pip install -r requirements.txt
```

### Запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск конкретного файла тестов

```bash
pytest tests/test_auth.py
```

### Запуск конкретного теста

```bash
pytest tests/test_auth.py::TestSendCode::test_send_code_success
```

### Запуск с покрытием кода

```bash
pytest --cov=app --cov-report=html
```

## Структура тестов

- `tests/conftest.py` - Конфигурация pytest, фикстуры
- `tests/test_auth.py` - Тесты эндпоинтов авторизации
- `tests/test_users.py` - Тесты эндпоинтов пользователей
- `tests/test_admin.py` - Тесты эндпоинтов администратора
- `tests/test_security.py` - Тесты безопасности
- `tests/test_crud.py` - Тесты CRUD операций

## Фикстуры

- `client` - Тестовый HTTP клиент
- `db_session` - Сессия базы данных для тестов
- `test_user` - Тестовый пользователь
- `test_admin` - Тестовый администратор
- `user_token` - JWT токен для пользователя
- `admin_token` - JWT токен для администратора

## Примечания

- Тесты используют SQLite в памяти для изоляции
- Каждый тест получает чистую базу данных
- Тесты не требуют реального подключения к PostgreSQL

