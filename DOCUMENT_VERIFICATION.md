# Инструкция по проверке документов

Документация по эндпоинтам для проверки документов пользователей (паспорт и водительские права).

---

## Для администратора

Все эндпоинты требуют авторизации администратора. Добавьте заголовок:
```
Authorization: Bearer <ваш_токен_администратора>
```

---

### 1. Одобрение паспорта пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/passport/approve`

**Описание:** Одобряет загруженный паспорт пользователя. Устанавливает статус верификации в `true`. Фото остается на сервере.

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример запроса (curl):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/passport/approve" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
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

**Ошибки:**
- `404 Not Found` - пользователь или профиль не найден
- `400 Bad Request` - у пользователя нет загруженного фото паспорта
- `401 Unauthorized` - неверный или отсутствующий токен
- `403 Forbidden` - недостаточно прав (не администратор)

---

### 2. Отклонение паспорта пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/passport/reject`

**Описание:** Отклоняет загруженный паспорт пользователя. **Удаляет фото с сервера**, сбрасывает статус верификации и дату загрузки.

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример запроса (curl):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/passport/reject" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
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

**Что происходит при отклонении:**
1. ✅ Фото паспорта удаляется с сервера
2. ✅ `passport_image_url` устанавливается в `null`
3. ✅ `passport_verified` устанавливается в `false`
4. ✅ `passport_uploaded_at` устанавливается в `null`

**Ошибки:**
- `404 Not Found` - пользователь или профиль не найден
- `401 Unauthorized` - неверный или отсутствующий токен
- `403 Forbidden` - недостаточно прав (не администратор)

---

### 3. Одобрение водительских прав пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/approve`

**Описание:** Одобряет загруженные водительские права пользователя. Устанавливает статус верификации в `true`. Фото остается на сервере.

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример запроса (curl):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/approve" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
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

**Ошибки:**
- `404 Not Found` - пользователь или профиль не найден
- `400 Bad Request` - у пользователя нет загруженного фото водительских прав
- `401 Unauthorized` - неверный или отсутствующий токен
- `403 Forbidden` - недостаточно прав (не администратор)

---

### 4. Отклонение водительских прав пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/reject`

**Описание:** Отклоняет загруженные водительские права пользователя. **Удаляет фото с сервера**, сбрасывает статус верификации и дату загрузки.

**Тело запроса:**
```json
{
  "phone_number": "+998900000000"
}
```

**Пример запроса (curl):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/user/documents/driving-license/reject" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+998900000000"
  }'
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

**Что происходит при отклонении:**
1. ✅ Фото водительских прав удаляется с сервера
2. ✅ `driving_license_image_url` устанавливается в `null`
3. ✅ `driving_license_verified` устанавливается в `false`
4. ✅ `driving_license_uploaded_at` устанавливается в `null`

**Ошибки:**
- `404 Not Found` - пользователь или профиль не найден
- `401 Unauthorized` - неверный или отсутствующий токен
- `403 Forbidden` - недостаточно прав (не администратор)

---

## Для пользователя

Все эндпоинты требуют авторизации пользователя. Добавьте заголовок:
```
Authorization: Bearer <ваш_токен>
```

---

### 1. Загрузка фото паспорта

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/passport`

**Описание:** Загружает или обновляет фото паспорта пользователя. После загрузки статус верификации автоматически сбрасывается на `false` до проверки администратором.

**Тип запроса:** `multipart/form-data`

**Параметры:**
- `file` (обязательно) - файл изображения паспорта

**Поддерживаемые форматы:**
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WEBP (.webp)

**Максимальный размер файла:** 5 MB

**Пример запроса (curl):**
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/profile/passport" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/passport.jpg"
```

**Пример запроса (JavaScript/Fetch):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:8000/api/v1/profile/passport', {
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
  "message": "Фото паспорта успешно загружено",
  "data": {
    "passport_image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
    "passport_verified": false,
    "uploaded_at": "2024-01-15T10:30:00Z"
  }
}
```

**Важно:**
- После загрузки нового фото статус верификации автоматически сбрасывается на `false`
- Если у пользователя уже было загружено фото, оно будет заменено новым
- Старое фото удаляется с сервера при загрузке нового

**Ошибки:**
- `400 Bad Request` - неверный формат файла или превышен размер
- `401 Unauthorized` - неверный или отсутствующий токен
- `404 Not Found` - профиль не найден (будет создан автоматически)

---

### 2. Загрузка фото водительских прав

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile/driving-license`

**Описание:** Загружает или обновляет фото водительских прав пользователя. После загрузки статус верификации автоматически сбрасывается на `false` до проверки администратором.

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
    "driving_license_image_url": "http://localhost:8000/uploads/driving_licenses/1_xyz789.jpg",
    "driving_license_verified": false,
    "uploaded_at": "2024-01-15T10:30:00Z"
  }
}
```

**Важно:**
- После загрузки нового фото статус верификации автоматически сбрасывается на `false`
- Если у пользователя уже было загружено фото, оно будет заменено новым
- Старое фото удаляется с сервера при загрузке нового

**Ошибки:**
- `400 Bad Request` - неверный формат файла или превышен размер
- `401 Unauthorized` - неверный или отсутствующий токен
- `404 Not Found` - профиль не найден (будет создан автоматически)

---

### 3. Получение статуса документов

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/profile`

**Описание:** Возвращает полную информацию о профиле пользователя, включая статус документов.

**Пример запроса (curl):**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Пример ответа (фрагмент с документами):**
```json
{
  "id": 1,
  "phone": "+998900000000",
  "name": "Иван Иванов",
  "profile": {
    "documents": {
      "passport": {
        "image_url": "http://localhost:8000/uploads/passports/1_abc123.jpg",
        "verified": true,
        "uploaded_at": "2024-01-15T10:30:00Z"
      },
      "driving_license": {
        "image_url": "http://localhost:8000/uploads/driving_licenses/1_xyz789.jpg",
        "verified": false,
        "uploaded_at": "2024-01-15T11:00:00Z"
      }
    }
  }
}
```

**Статусы документов:**
- `verified: true` - документ одобрен администратором
- `verified: false` - документ ожидает проверки или был отклонен
- `image_url: null` - документ не загружен или был отклонен (фото удалено)

---

## Процесс проверки документов

### Шаг 1: Пользователь загружает документ
Пользователь загружает фото паспорта или водительских прав через соответствующий эндпоинт:
- `PATCH /api/v1/profile/passport`
- `PATCH /api/v1/profile/driving-license`

После загрузки:
- ✅ Фото сохраняется на сервере
- ✅ `verified` устанавливается в `false` (ожидает проверки)
- ✅ `uploaded_at` устанавливается в текущую дату и время

### Шаг 2: Администратор проверяет документ
Администратор просматривает загруженные документы и принимает решение:

**Одобрить документ:**
- `POST /api/v1/admin/user/documents/passport/approve`
- `POST /api/v1/admin/user/documents/driving-license/approve`

Результат:
- ✅ `verified` устанавливается в `true`
- ✅ Фото остается на сервере
- ✅ Пользователь может использовать документ

**Отклонить документ:**
- `POST /api/v1/admin/user/documents/passport/reject`
- `POST /api/v1/admin/user/documents/driving-license/reject`

Результат:
- ✅ Фото удаляется с сервера
- ✅ `image_url` устанавливается в `null`
- ✅ `verified` устанавливается в `false`
- ✅ `uploaded_at` устанавливается в `null`
- ✅ Пользователь должен загрузить документ заново

### Шаг 3: Пользователь проверяет статус
Пользователь может проверить статус своих документов через:
- `GET /api/v1/profile`

---

## Примеры использования (Python)

### Для администратора

```python
import requests

BASE_URL = "http://127.0.0.1:8000"
ADMIN_TOKEN = "your_admin_token"

# Одобрить паспорт
response = requests.post(
    f"{BASE_URL}/api/v1/admin/user/documents/passport/approve",
    headers={
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    },
    json={"phone_number": "+998900000000"}
)
print(response.json())

# Отклонить водительские права
response = requests.post(
    f"{BASE_URL}/api/v1/admin/user/documents/driving-license/reject",
    headers={
        "Authorization": f"Bearer {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    },
    json={"phone_number": "+998900000000"}
)
print(response.json())
```

### Для пользователя

```python
import requests

BASE_URL = "http://127.0.0.1:8000"
USER_TOKEN = "your_user_token"

# Загрузить фото паспорта
with open("passport.jpg", "rb") as f:
    files = {"file": f}
    response = requests.patch(
        f"{BASE_URL}/api/v1/profile/passport",
        headers={"Authorization": f"Bearer {USER_TOKEN}"},
        files=files
    )
    print(response.json())

# Проверить статус документов
response = requests.get(
    f"{BASE_URL}/api/v1/profile",
    headers={"Authorization": f"Bearer {USER_TOKEN}"}
)
profile = response.json()
print(f"Паспорт: {'Одобрен' if profile['profile']['documents']['passport']['verified'] else 'Ожидает проверки'}")
print(f"Права: {'Одобрены' if profile['profile']['documents']['driving_license']['verified'] else 'Ожидают проверки'}")
```

---

## Примеры использования (Flutter/Dart)

### Для пользователя

```dart
import 'package:http/http.dart' as http;
import 'dart:io';

// Загрузка фото паспорта
Future<void> uploadPassport(File imageFile, String token) async {
  var request = http.MultipartRequest(
    'PATCH',
    Uri.parse('http://127.0.0.1:8000/api/v1/profile/passport'),
  );
  
  request.headers['Authorization'] = 'Bearer $token';
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path),
  );
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  print(responseData);
}

// Проверка статуса документов
Future<Map<String, dynamic>> getProfile(String token) async {
  final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/api/v1/profile'),
    headers: {'Authorization': 'Bearer $token'},
  );
  
  return jsonDecode(response.body);
}
```

---

## Важные замечания

1. **Безопасность:**
   - Все эндпоинты требуют авторизации
   - Только администраторы могут одобрять/отклонять документы
   - Пользователи могут только загружать документы

2. **Файлы:**
   - Максимальный размер: 5 MB
   - Разрешенные типы: JPEG, PNG, WEBP
   - Файлы сохраняются в директориях `uploads/passports/` и `uploads/driving_licenses/`

3. **Статусы:**
   - `verified: false` - документ ожидает проверки или был отклонен
   - `verified: true` - документ одобрен администратором
   - `image_url: null` - документ не загружен или был отклонен (фото удалено)

4. **Отклонение документа:**
   - При отклонении фото **полностью удаляется** с сервера
   - Пользователь должен загрузить документ заново
   - Все данные документа сбрасываются (image_url, verified, uploaded_at)

5. **Автоматическое создание:**
   - Если у пользователя нет профиля, он будет создан автоматически при первой загрузке документа

---

## Полный список эндпоинтов

### Администратор
| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `/api/v1/admin/user/documents/passport/approve` | POST | Одобрить паспорт |
| `/api/v1/admin/user/documents/passport/reject` | POST | Отклонить паспорт (удалить фото) |
| `/api/v1/admin/user/documents/driving-license/approve` | POST | Одобрить водительские права |
| `/api/v1/admin/user/documents/driving-license/reject` | POST | Отклонить водительские права (удалить фото) |

### Пользователь
| Эндпоинт | Метод | Описание |
|----------|-------|----------|
| `/api/v1/profile/passport` | PATCH | Загрузить/обновить фото паспорта |
| `/api/v1/profile/driving-license` | PATCH | Загрузить/обновить фото водительских прав |
| `/api/v1/profile` | GET | Получить профиль со статусом документов |






