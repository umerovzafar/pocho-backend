# API для Flutter

## Базовый URL
```
http://your-server.com/api/v1
```

## Авторизация

### Получение токена (пользователь)
1. `POST /auth/send-code`
   ```dart
   {
     "phone_number": "+998900000000" // String
   }
   ```

2. `POST /auth/verify-code`
   ```dart
   {
     "phone_number": "+998900000000", // String
     "code": "1234" // String (4 цифры)
   }
   ```
   **Ответ:** `{"access_token": "...", "token_type": "bearer"}`

## Использование токена

Добавляйте в заголовки всех защищенных запросов:
```dart
headers: {
  "Authorization": "Bearer $token",
  "Content-Type": "application/json"
}
```

## Эндпоинты

### Пользователь

**GET /users/me** - Информация о текущем пользователе
- Требует: `Authorization: Bearer <token>`
- Ответ: `UserResponse`

**GET /users/{user_id}** - Получить пользователя по ID
- Требует: `Authorization: Bearer <token>`
- Ответ: `UserResponse`

**POST /auth/logout** - Выход из системы
- Требует: `Authorization: Bearer <token>`
- Ответ: `{"message": "...", "success": true}`

## Типы данных

### UserResponse
```dart
{
  "id": 0,                    // int
  "phone_number": "string",   // String
  "fullname": "string",       // String?
  "is_active": true,          // bool
  "is_admin": false,          // bool
  "is_blocked": false,        // bool
  "created_at": "2024-01-01T00:00:00" // DateTime
}
```

## Обработка ошибок

- `200` - Успех
- `400` - Неверный запрос
- `401` - Не авторизован
- `403` - Доступ запрещен
- `404` - Не найдено
- `422` - Ошибка валидации
- `429` - Превышен лимит запросов
- `500` - Ошибка сервера

**Формат ошибки:**
```dart
{
  "detail": "Сообщение об ошибке"
}
```

## Примеры запросов

### Flutter/Dart

```dart
// Отправка SMS кода
final response = await http.post(
  Uri.parse('$baseUrl/auth/send-code'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'phone_number': '+998900000000'}),
);

// Верификация кода
final response = await http.post(
  Uri.parse('$baseUrl/auth/verify-code'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'phone_number': '+998900000000',
    'code': '1234'
  }),
);
final token = jsonDecode(response.body)['token']['access_token'];

// Защищенный запрос
final response = await http.get(
  Uri.parse('$baseUrl/users/me'),
  headers: {
    'Authorization': 'Bearer $token',
    'Content-Type': 'application/json',
  },
);
```

## Важно

- Все номера телефонов: формат `+998XXXXXXXXX`
- Коды верификации: 4 цифры
- Токены действительны 30 минут
- После logout токен становится недействительным
- Rate limit: 60 запросов/минуту (обычные), 5 запросов/минуту (auth)
