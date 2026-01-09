# Эндпоинты профиля пользователя

Все эндпоинты требуют авторизации пользователя. Добавьте заголовок:
```
Authorization: Bearer <ваш_токен>
```

---

## 1. Обновление фото водительских прав

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/driving-license`

**Тип запроса:** `multipart/form-data`

**Параметры:**
- `file` (обязательно) - файл изображения водительских прав

**Поддерживаемые форматы:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

**Максимальный размер файла:** 5 MB

**Пример запроса (curl):**
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/profile/driving-license" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/driving_license.jpg"
```

**Пример запроса (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/v1/profile/driving-license', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Фото водительских прав успешно загружено",
  "data": {
    "driving_license_image_url": "http://localhost:8000/uploads/driving_licenses/1_abc123.jpg",
    "driving_license_verified": false,
    "uploaded_at": "2024-01-15T10:30:00Z"
  }
}
```

**Примечания:**
- После загрузки нового фото статус верификации автоматически сбрасывается на `false`
- Файл сохраняется в директории `uploads/driving_licenses/`
- Имя файла генерируется автоматически: `{user_id}_{uuid}.{extension}`

---

## 2. Обновление настроек уведомлений

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/notifications`

**Тип запроса:** `application/json`

**Тело запроса:**
```json
{
  "notifications_enabled": true
}
```

**Параметры:**
- `notifications_enabled` (обязательно) - `boolean` - включить/выключить уведомления

**Пример запроса (curl):**
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/profile/notifications" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notifications_enabled": true
  }'
```

**Пример запроса (JavaScript/Fetch):**
```javascript
fetch('http://127.0.0.1:8000/api/v1/profile/notifications', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    notifications_enabled: true
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Настройки уведомлений успешно обновлены",
  "data": {
    "notifications_enabled": true
  }
}
```

**Примечания:**
- Изменяет только статус уведомлений, остальные настройки профиля не затрагиваются
- Значение по умолчанию: `true` (уведомления включены)

---

## 3. Обновление аватара пользователя

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/avatar`

**Тип запроса:** `multipart/form-data`

**Параметры:**
- `file` (обязательно) - файл изображения аватара

**Поддерживаемые форматы:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

**Максимальный размер файла:** 5 MB

**Пример запроса (curl):**
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/profile/avatar" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/avatar.jpg"
```

**Пример запроса (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/v1/profile/avatar', {
  method: 'PATCH',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Пример ответа:**
```json
{
  "success": true,
  "message": "Аватар успешно обновлен",
  "data": {
    "avatar": "http://localhost:8000/uploads/avatars/1_abc123.jpg"
  }
}
```

**Примечания:**
- При загрузке нового аватара старый автоматически удаляется с сервера
- Файл сохраняется в директории `uploads/avatars/`
- Имя файла генерируется автоматически: `{user_id}_{uuid}.{extension}`
- Аватар отображается в профиле пользователя

---

## Дополнительные эндпоинты профиля

### Получение профиля
**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile`

Возвращает полную информацию о профиле пользователя, включая баланс, уровень, рейтинг, документы и настройки.

### Обновление имени
**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/name`

**Тело запроса:**
```json
{
  "name": "Иван Иванов"
}
```

### Обновление email
**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/email`

**Тело запроса:**
```json
{
  "email": "user@example.com"
}
```

### Обновление фото паспорта
**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/passport`

Аналогично обновлению водительских прав, но для паспорта.

---

## Важные замечания

1. **Авторизация:** Все запросы требуют токен пользователя в заголовке `Authorization: Bearer <token>`

2. **Ошибки:**
   - `401 Unauthorized` - неверный или отсутствующий токен
   - `404 Not Found` - профиль не найден (будет создан автоматически)
   - `400 Bad Request` - неверный формат файла или превышен размер
   - `422 Unprocessable Entity` - ошибка валидации данных

3. **Автоматическое создание:** Если у пользователя нет расширенного профиля, он будет создан автоматически при первом обращении

4. **Файлы:**
   - Максимальный размер: 5 MB
   - Разрешенные типы: JPEG, PNG, WEBP
   - Файлы сохраняются на сервере и доступны по URL

5. **Верификация документов:** После загрузки нового фото документов статус верификации автоматически сбрасывается на `false`. Администратор может изменить статус через эндпоинт `/api/v1/admin/user/documents`

6. **Аватар:** При загрузке нового аватара старый автоматически удаляется с сервера для экономии места

---

## Примеры использования

### Загрузка фото водительских прав (Python requests)
```python
import requests

url = "http://127.0.0.1:8000/api/v1/profile/driving-license"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

with open("driving_license.jpg", "rb") as f:
    files = {"file": f}
    response = requests.patch(url, headers=headers, files=files)
    print(response.json())
```

### Включение уведомлений (Python requests)
```python
import requests

url = "http://127.0.0.1:8000/api/v1/profile/notifications"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "Content-Type": "application/json"
}
data = {"notifications_enabled": True}

response = requests.patch(url, headers=headers, json=data)
print(response.json())
```

### Загрузка аватара (Python requests)
```python
import requests

url = "http://127.0.0.1:8000/api/v1/profile/avatar"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

with open("avatar.jpg", "rb") as f:
    files = {"file": f}
    response = requests.patch(url, headers=headers, files=files)
    print(response.json())
```

### Загрузка фото водительских прав (Flutter/Dart)
```dart
import 'package:http/http.dart' as http;
import 'dart:io';

Future<void> uploadDrivingLicense(File imageFile, String token) async {
  var request = http.MultipartRequest(
    'PATCH',
    Uri.parse('http://127.0.0.1:8000/api/v1/profile/driving-license'),
  );
  
  request.headers['Authorization'] = 'Bearer $token';
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  print(responseData);
}
```

### Обновление уведомлений (Flutter/Dart)
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> updateNotifications(bool enabled, String token) async {
  final response = await http.patch(
    Uri.parse('http://127.0.0.1:8000/api/v1/profile/notifications'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'notifications_enabled': enabled,
    }),
  );
  
  print(jsonDecode(response.body));
}
```

### Загрузка аватара (Flutter/Dart)
```dart
import 'package:http/http.dart' as http;
import 'dart:io';

Future<void> uploadAvatar(File imageFile, String token) async {
  var request = http.MultipartRequest(
    'PATCH',
    Uri.parse('http://127.0.0.1:8000/api/v1/profile/avatar'),
  );
  
  request.headers['Authorization'] = 'Bearer $token';
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  print(responseData);
}
```

