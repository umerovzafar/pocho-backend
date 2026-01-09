# Эндпоинты администратора для управления профилями пользователей

Все эндпоинты требуют авторизации администратора. Добавьте заголовок:
```
Authorization: Bearer <ваш_токен_администратора>
```

---

## 1. Обновление имени пользователя (ФИО)

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/name`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000",
  "name": "Иван Иванов"
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Имя пользователя успешно обновлено",
  "data": {
    "name": "Иван Иванов",
    "phone_number": "+998900000000"
  }
}
```

---

## 2. Обновление баланса пользователя

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/balance`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000",
  "balance": 150000.0
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Баланс пользователя успешно обновлен",
  "data": {
    "balance": 150000.0,
    "balance_info": {
      "amount": 150000.0,
      "currency": "сум",
      "formatted": "150.0 тыс сум"
    },
    "phone_number": "+998900000000"
  }
}
```

---

## 3. Обновление рейтинга пользователя

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/rating`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000",
  "rating": 4.5
}
```

**Валидация:** рейтинг должен быть от 0 до 5

**Пример ответа:**
```json
{
  "success": true,
  "message": "Рейтинг пользователя успешно обновлен",
  "data": {
    "rating": 4.5,
    "phone_number": "+998900000000"
  }
}
```

---

## 4. Обновление уровня пользователя

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/level`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000",
  "level": "Золотой"
}
```

**Доступные уровни:**
- "Новичок"
- "Серебряный"
- "Золотой"
- "Платиновый"

**Пример ответа:**
```json
{
  "success": true,
  "message": "Уровень пользователя успешно обновлен",
  "data": {
    "level": "Золотой",
    "phone_number": "+998900000000"
  }
}
```

---

## 5. Обновление статуса документов пользователя

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000",
  "passport_verified": true,
  "driving_license_verified": false
}
```

**Примечание:** Оба поля (`passport_verified` и `driving_license_verified`) опциональны, но нужно указать хотя бы одно.

**Пример ответа:**
```json
{
  "success": true,
  "message": "Статус документов пользователя успешно обновлен",
  "data": {
    "documents": {
      "passport": {
        "image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      },
      "driving_license": {
        "image_url": null,
        "verified": false,
        "uploaded_at": null
      }
    },
    "phone_number": "+998900000000"
  }
}
```

---

## 6. Одобрение паспорта пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/passport/approve`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Паспорт пользователя одобрен",
  "data": {
    "documents": {
      "passport": {
        "image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      },
      "driving_license": {
        "image_url": null,
        "verified": false,
        "uploaded_at": null
      }
    },
    "phone_number": "+998900000000"
  }
}
```

**Примечание:** Устанавливает статус верификации паспорта в `true`. Фото остается на сервере.

---

## 7. Отклонение паспорта пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/passport/reject`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Паспорт пользователя отклонен, фото удалено",
  "data": {
    "documents": {
      "passport": {
        "image_url": null,
        "verified": false,
        "uploaded_at": null
      },
      "driving_license": {
        "image_url": "http://localhost:8000/uploads/driving_licenses/1_xyz789.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      }
    },
    "phone_number": "+998900000000"
  }
}
```

**Примечание:** 
- Удаляет фото паспорта с сервера
- Сбрасывает `image_url` в `null`
- Устанавливает `verified` в `false`
- Сбрасывает `uploaded_at` в `null`

---

## 8. Одобрение водительских прав пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/approve`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Водительские права пользователя одобрены",
  "data": {
    "documents": {
      "passport": {
        "image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      },
      "driving_license": {
        "image_url": "http://localhost:8000/uploads/driving_licenses/1_xyz789.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      }
    },
    "phone_number": "+998900000000"
  }
}
```

**Примечание:** Устанавливает статус верификации водительских прав в `true`. Фото остается на сервере.

---

## 9. Отклонение водительских прав пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/reject`

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Водительские права пользователя отклонены, фото удалено",
  "data": {
    "documents": {
      "passport": {
        "image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      },
      "driving_license": {
        "image_url": null,
        "verified": false,
        "uploaded_at": null
      }
    },
    "phone_number": "+998900000000"
  }
}
```

**Примечание:** 
- Удаляет фото водительских прав с сервера
- Сбрасывает `image_url` в `null`
- Устанавливает `verified` в `false`
- Сбрасывает `uploaded_at` в `null`

---

## Примеры использования с curl

### Обновление имени
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/user/name" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000",
    "name": "Иван Иванов"
  }'
```

### Обновление баланса
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/user/balance" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000",
    "balance": 200000.0
  }'
```

### Обновление рейтинга
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/user/rating" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000",
    "rating": 4.8
  }'
```

### Обновление уровня
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/user/level" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000",
    "level": "Платиновый"
  }'
```

### Обновление документов
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/admin/user/documents" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000",
    "passport_verified": true,
    "driving_license_verified": true
  }'
```

### Одобрение паспорта
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/passport/approve" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
```

### Отклонение паспорта
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/passport/reject" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
```

### Одобрение водительских прав
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/approve" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
```

### Отклонение водительских прав
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/reject" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
```

---

## Важные замечания

1. **Авторизация:** Все запросы требуют токен администратора в заголовке `Authorization: Bearer <token>`

2. **Формат номера телефона:** Номер должен быть в узбекском формате: `+998XXXXXXXXX` (9 цифр после +998)

3. **Валидация:**
   - Имя: от 1 до 100 символов
   - Баланс: неотрицательное число
   - Рейтинг: от 0 до 5
   - Уровень: любая строка (рекомендуется использовать стандартные значения)

4. **Ошибки:**
   - `404 Not Found` - пользователь не найден
   - `401 Unauthorized` - неверный или отсутствующий токен
   - `403 Forbidden` - недостаточно прав (не администратор)
   - `422 Unprocessable Entity` - ошибка валидации данных

5. **Автоматическое создание:** Если у пользователя нет расширенного профиля, он будет создан автоматически при первом обновлении

---

## Полный список эндпоинтов администратора

| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `/api/v1/admin/user/name` | PATCH | Обновление имени пользователя |
| `/api/v1/admin/user/balance` | PATCH | Обновление баланса пользователя |
| `/api/v1/admin/user/rating` | PATCH | Обновление рейтинга пользователя |
| `/api/v1/admin/user/level` | PATCH | Обновление уровня пользователя |
| `/api/v1/admin/user/documents` | PATCH | Обновление статуса документов |
| `/api/v1/admin/user/documents/passport/approve` | POST | Одобрение паспорта пользователя |
| `/api/v1/admin/user/documents/passport/reject` | POST | Отклонение паспорта пользователя (удаление фото) |
| `/api/v1/admin/user/documents/driving-license/approve` | POST | Одобрение водительских прав пользователя |
| `/api/v1/admin/user/documents/driving-license/reject` | POST | Отклонение водительских прав пользователя (удаление фото) |
| `/api/v1/admin/users` | GET | Получение списка всех пользователей |
| `/api/v1/admin/user` | DELETE | Удаление пользователя |
| `/api/v1/admin/user/admin` | POST | Назначение/снятие прав администратора |
| `/api/v1/admin/user/block` | POST | Блокировка/разблокировка пользователя |
| `/api/v1/admin/create-admin` | POST | Создание нового администратора |

