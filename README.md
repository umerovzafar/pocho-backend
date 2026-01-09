# Pocho Backend API

FastAPI приложение с авторизацией и интеграцией PostgreSQL.

## Установка

1. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. Создайте `.env` файл (см. `.env.example`) и настройте:
- `DATABASE_URL` - подключение к PostgreSQL
- `SECRET_KEY` - секретный ключ для JWT
- `SMS_API_URL`, `SMS_AUTH_EMAIL`, `SMS_AUTH_SECRET_KEY` - настройки SMS

3. Создайте базу данных и запустите:
```bash
python run.py
```

API доступен: http://localhost:8000  
Документация: http://localhost:8000/docs

## API Эндпоинты

### Авторизация

#### `POST /api/v1/auth/send-code`
Отправка SMS кода на номер телефона.

**Запрос:**
```json
{
  "phone_number": "string" // +998XXXXXXXXX
}
```

**Ответ:**
```json
{
  "message": "string",
  "phone_number": "string",
  "expires_in": 300
}
```

#### `POST /api/v1/auth/verify-code`
Верификация кода и авторизация (автоматическая регистрация).

**Запрос:**
```json
{
  "phone_number": "string", // +998XXXXXXXXX
  "code": "string" // 4 цифры
}
```

**Ответ:**
```json
{
  "is_verified": true,
  "message": "string",
  "token": {
    "access_token": "string",
    "token_type": "bearer"
  }
}
```

#### `POST /api/v1/auth/check-registration`
Проверка регистрации пользователя.

**Запрос:**
```json
{
  "phone_number": "string"
}
```

**Ответ:**
```json
{
  "is_registered": true,
  "phone_number": "string"
}
```

#### `POST /api/v1/auth/admin/login`
Авторизация администратора по логину и паролю.

**Запрос:**
```json
{
  "login": "string",
  "password": "string"
}
```

**Ответ:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### `POST /api/v1/auth/logout`
Выход пользователя из системы.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "message": "string",
  "success": true
}
```

#### `POST /api/v1/auth/admin/logout`
Выход администратора из системы.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "message": "string",
  "success": true
}
```

### Пользователи

#### `GET /api/v1/users/me`
Получение информации о текущем пользователе.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:**
```json
{
  "id": 0,
  "phone_number": "string",
  "fullname": "string",
  "is_active": true,
  "is_admin": false,
  "is_blocked": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### `GET /api/v1/users/{user_id}`
Получение пользователя по ID.

**Заголовки:** `Authorization: Bearer <token>`

**Ответ:** (как в `/users/me`)

### Администрирование

#### `POST /api/v1/admin/create-admin`
Создание нового администратора.

**Заголовки:** `Authorization: Bearer <admin_token>`

**Запрос:**
```json
{
  "phone_number": "string"
}
```

**Ответ:**
```json
{
  "message": "string",
  "phone_number": "string",
  "login": "string",
  "password": "string",
  "user": { /* UserResponse */ }
}
```

#### `DELETE /api/v1/admin/user`
Удаление пользователя.

**Заголовки:** `Authorization: Bearer <admin_token>`

**Запрос:**
```json
{
  "phone_number": "string"
}
```

**Ответ:**
```json
{
  "message": "string",
  "phone_number": "string",
  "deleted": true
}
```

#### `POST /api/v1/admin/user/admin`
Назначение/снятие прав администратора.

**Заголовки:** `Authorization: Bearer <admin_token>`

**Запрос:**
```json
{
  "phone_number": "string",
  "is_admin": true
}
```

**Ответ:**
```json
{
  "message": "string",
  "user": { /* UserResponse */ }
}
```

#### `POST /api/v1/admin/user/block`
Блокировка/разблокировка пользователя.

**Заголовки:** `Authorization: Bearer <admin_token>`

**Запрос:**
```json
{
  "phone_number": "string",
  "is_blocked": true
}
```

**Ответ:**
```json
{
  "message": "string",
  "user": { /* UserResponse */ }
}
```

## Последовательность запросов

### Авторизация пользователя:
1. `POST /api/v1/auth/send-code` → получить SMS код
2. `POST /api/v1/auth/verify-code` → получить JWT токен
3. Использовать токен в заголовке `Authorization: Bearer <token>`

### Авторизация администратора:
1. `POST /api/v1/auth/admin/login` → получить JWT токен
2. Использовать токен в заголовке `Authorization: Bearer <token>`

### Создание администратора:
1. Авторизоваться как существующий администратор
2. `POST /api/v1/admin/create-admin` → получить логин и пароль
3. Использовать логин/пароль для авторизации

## Тестирование

```bash
pytest
```

Подробнее: `tests/README.md`

## Безопасность

Подробнее: `SECURITY.md`

## Дополнительная документация

- `SMS_SETUP.md` - Настройка SMS сервиса
- `SECURITY.md` - Меры безопасности
- `tests/README.md` - Инструкции по тестированию
