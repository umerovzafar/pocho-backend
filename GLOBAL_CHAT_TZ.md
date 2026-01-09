# Техническое задание: Глобальный чат

## Общее описание

Глобальный чат на WebSocket для всех пользователей приложения с поддержкой файлов, блокировки пользователей, поиска и персонального удаления истории.

---

## 1. Архитектура системы

### 1.1. Модели базы данных

**Таблица `global_chat_messages`:**
- `id` - первичный ключ
- `user_id` - ID пользователя, отправившего сообщение
- `message_type` - тип сообщения (text, image, video, file, audio)
- `message` - текст сообщения (может быть NULL для медиа-файлов)
- `attachments` - JSON массив прикрепленных файлов
- `metadata` - дополнительные метаданные (JSON)
- `created_at` - дата создания
- `updated_at` - дата обновления
- `deleted_at` - дата удаления (мягкое удаление для всех)

**Таблица `user_blocks`:**
- `id` - первичный ключ
- `blocker_id` - ID пользователя, который блокирует
- `blocked_id` - ID пользователя, которого блокируют
- `created_at` - дата блокировки

**Таблица `hidden_global_chat_messages`:**
- `id` - первичный ключ
- `message_id` - ID сообщения
- `user_id` - ID пользователя, для которого скрыто
- `hidden_at` - дата скрытия

### 1.2. Типы сообщений

- **TEXT** - текстовое сообщение
- **IMAGE** - изображение
- **VIDEO** - видео
- **FILE** - файл
- **AUDIO** - аудио

---

## 2. WebSocket эндпоинт

### 2.1. Подключение к глобальному чату

**WebSocket URL:** `ws://127.0.0.1:8000/api/v1/global-chat/ws?token=<jwt_token>`

**После подключения:**
```json
{
  "type": "connection",
  "status": "connected",
  "user_id": 123,
  "online_count": 15,
  "message": "Подключено к глобальному чату"
}
```

### 2.2. Получение нового сообщения

**Формат:**
```json
{
  "type": "new_message",
  "message": {
    "id": 1,
    "user_id": 123,
    "user_name": "Иван Иванов",
    "user_avatar": "http://localhost:8000/uploads/avatars/123_abc.jpg",
    "message": "Привет всем!",
    "message_type": "text",
    "attachments": null,
    "metadata": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": null
  }
}
```

### 2.3. Обновление количества онлайн

**Формат:**
```json
{
  "type": "online_count",
  "online_count": 15,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2.4. Удаление сообщения

**Формат:**
```json
{
  "type": "message_deleted",
  "message_id": 1
}
```

### 2.5. Поддержание соединения

Клиент может отправлять `"ping"` для поддержания соединения:
```json
"ping"
```

Сервер отвечает:
```json
{
  "type": "pong"
}
```

---

## 3. REST API эндпоинты

### 3.1. Отправка сообщения

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages`

**Тело запроса (текстовое сообщение):**
```json
{
  "message": "Привет всем!",
  "message_type": "text",
  "attachments": null,
  "metadata": null
}
```

**Тело запроса (с файлом):**
```json
{
  "message": "Смотрите фото!",
  "message_type": "image",
  "attachments": [
    {
      "url": "http://localhost:8000/uploads/global_chat/images/123_abc.jpg",
      "type": "image",
      "name": "photo.jpg",
      "size": 123456
    }
  ],
  "metadata": null
}
```

**Ответ:**
```json
{
  "id": 1,
  "user_id": 123,
  "user_name": "Иван Иванов",
  "user_avatar": "http://localhost:8000/uploads/avatars/123_abc.jpg",
  "message": "Привет всем!",
  "message_type": "text",
  "attachments": null,
  "metadata": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null
}
```

### 3.2. Загрузка файла

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages/upload`

**Тип запроса:** `multipart/form-data`

**Параметры:**
- `file` (обязательно) - файл для загрузки
- `file_type` (обязательно, query) - тип файла: `image`, `video`, `audio`, `file`

**Поддерживаемые форматы:**
- Изображения: JPEG, PNG, WEBP, GIF
- Видео: MP4, AVI, MOV, WEBM
- Аудио: MP3, WAV, OGG
- Файлы: любые другие типы

**Максимальный размер файла:** 50 MB

**Пример запроса (curl):**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/global-chat/messages/upload?file_type=image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/photo.jpg"
```

**Ответ:**
```json
{
  "success": true,
  "file_url": "http://localhost:8000/uploads/global_chat/images/123_abc.jpg",
  "attachment": {
    "url": "http://localhost:8000/uploads/global_chat/images/123_abc.jpg",
    "type": "image",
    "name": "photo.jpg",
    "size": 123456
  },
  "message_type": "image"
}
```

### 3.3. Получение сообщений

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages`

**Query параметры:**
- `skip` (int, default: 0) - количество пропущенных записей
- `limit` (int, default: 100, max: 1000) - максимальное количество записей

**Ответ:**
```json
{
  "messages": [
    {
      "id": 1,
      "user_id": 123,
      "user_name": "Иван Иванов",
      "user_avatar": "http://localhost:8000/uploads/avatars/123_abc.jpg",
      "message": "Привет всем!",
      "message_type": "text",
      "attachments": null,
      "metadata": null,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": null
    }
  ],
  "total": 50,
  "skip": 0,
  "limit": 100,
  "online_count": 15
}
```

**Примечание:** Автоматически исключаются:
- Удаленные сообщения
- Сообщения от заблокированных пользователей
- Скрытые сообщения (для текущего пользователя)

### 3.4. Поиск сообщений

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages/search`

**Query параметры:**
- `query` (string, обязательный) - поисковый запрос
- `skip` (int, default: 0)
- `limit` (int, default: 100, max: 1000)

**Ответ:**
```json
{
  "messages": [
    {
      "id": 5,
      "user_id": 123,
      "user_name": "Иван Иванов",
      "message": "Ищу информацию о заправках",
      "message_type": "text",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1,
  "query": "заправках",
  "skip": 0,
  "limit": 100
}
```

### 3.5. Получение количества онлайн

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/online`

**Ответ:**
```json
{
  "online_count": 15,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3.6. Блокировка пользователя

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/block`

**Тело запроса:**
```json
{
  "blocked_user_id": 456
}
```

**Ответ:**
```json
{
  "id": 1,
  "blocker_id": 123,
  "blocked_id": 456,
  "blocked_user_name": "Петр Петров",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Примечание:** После блокировки пользователь не будет видеть сообщения от заблокированного пользователя.

### 3.7. Разблокировка пользователя

**Метод:** `DELETE`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/block/{blocked_user_id}`

**Ответ:**
```json
{
  "success": true,
  "message": "Пользователь разблокирован"
}
```

### 3.8. Список заблокированных пользователей

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/blocked`

**Ответ:**
```json
{
  "blocked_users": [
    {
      "id": 1,
      "blocker_id": 123,
      "blocked_id": 456,
      "blocked_user_name": "Петр Петров",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 1
}
```

### 3.9. Очистка истории чата (только для текущего пользователя)

**Метод:** `DELETE`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages/history`

**Ответ:**
```json
{
  "success": true,
  "message": "История чата очищена (50 сообщений скрыто)",
  "count": 50
}
```

**Примечание:** История удаляется только для текущего пользователя. Остальные пользователи продолжат видеть все сообщения.

### 3.10. Удаление сообщения (для всех)

**Метод:** `DELETE`  
**Путь:** `http://127.0.0.1:8000/api/v1/global-chat/messages/{message_id}`

**Ответ:**
```json
{
  "success": true,
  "message": "Сообщение удалено",
  "message_id": 1
}
```

**Примечание:** Только автор сообщения может его удалить. Удаление происходит для всех пользователей.

---

## 4. Примеры использования

### 4.1. WebSocket подключение (JavaScript)

```javascript
const token = "YOUR_JWT_TOKEN";
const ws = new WebSocket(
  `ws://127.0.0.1:8000/api/v1/global-chat/ws?token=${token}`
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === "new_message") {
    console.log("Новое сообщение:", data.message);
    // Добавить сообщение в UI
  } else if (data.type === "online_count") {
    console.log("Онлайн пользователей:", data.online_count);
    // Обновить счетчик онлайн
  } else if (data.type === "connection") {
    console.log("Подключено к чату");
  }
};

// Отправка сообщения через REST API
async function sendMessage(text) {
  const response = await fetch(
    "http://127.0.0.1:8000/api/v1/global-chat/messages",
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: text,
        message_type: "text"
      })
    }
  );
  return await response.json();
}
```

### 4.2. Загрузка изображения (JavaScript)

```javascript
async function uploadImage(file) {
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/global-chat/messages/upload?file_type=image`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    }
  );
  
  const result = await response.json();
  
  // Отправляем сообщение с изображением
  await sendMessageWithAttachment(result.attachment, "image");
}

async function sendMessageWithAttachment(attachment, messageType) {
  const response = await fetch(
    "http://127.0.0.1:8000/api/v1/global-chat/messages",
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: "Смотрите фото!",
        message_type: messageType,
        attachments: [attachment]
      })
    }
  );
  return await response.json();
}
```

### 4.3. Блокировка пользователя (JavaScript)

```javascript
async function blockUser(userId) {
  const response = await fetch(
    "http://127.0.0.1:8000/api/v1/global-chat/block",
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        blocked_user_id: userId
      })
    }
  );
  return await response.json();
}
```

### 4.4. Поиск сообщений (JavaScript)

```javascript
async function searchMessages(query) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/global-chat/messages/search?query=${encodeURIComponent(query)}`,
    {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    }
  );
  return await response.json();
}
```

### 4.5. Flutter пример

```dart
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class GlobalChatService {
  WebSocketChannel? _channel;
  final String token;
  
  GlobalChatService(this.token);
  
  void connect() {
    final uri = Uri.parse(
      'ws://127.0.0.1:8000/api/v1/global-chat/ws?token=$token'
    );
    _channel = WebSocketChannel.connect(uri);
    
    _channel!.stream.listen(
      (message) {
        final data = jsonDecode(message);
        if (data['type'] == 'new_message') {
          _handleNewMessage(data['message']);
        } else if (data['type'] == 'online_count') {
          _updateOnlineCount(data['online_count']);
        }
      },
    );
    
    // Ping каждые 30 секунд
    Timer.periodic(Duration(seconds: 30), (_) {
      _channel?.sink.add('ping');
    });
  }
  
  Future<void> sendMessage(String text) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/v1/global-chat/messages'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'message': text,
        'message_type': 'text'
      }),
    );
    // Сообщение будет доставлено через WebSocket
  }
  
  Future<void> uploadFile(File file, String fileType) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://127.0.0.1:8000/api/v1/global-chat/messages/upload?file_type=$fileType'),
    );
    
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(
      await http.MultipartFile.fromPath('file', file.path),
    );
    
    var response = await request.send();
    var responseData = await response.stream.bytesToString();
    final result = jsonDecode(responseData);
    
    // Отправляем сообщение с файлом
    await sendMessageWithAttachment(result['attachment'], result['message_type']);
  }
  
  void disconnect() {
    _channel?.sink.close();
  }
}
```

---

## 5. Логика работы

### 5.1. Блокировка пользователей

- При блокировке пользователя все его сообщения скрываются для блокирующего
- Заблокированный пользователь не знает, что его заблокировали
- Можно разблокировать в любой момент

### 5.2. Удаление истории

- **Персональное удаление** (`DELETE /messages/history`): скрывает все сообщения только для текущего пользователя
- **Удаление сообщения** (`DELETE /messages/{id}`): удаляет сообщение для всех пользователей (только автор может удалить)

### 5.3. Поиск сообщений

- Поиск выполняется по тексту сообщения (case-insensitive)
- Автоматически исключаются заблокированные и скрытые сообщения
- Результаты сортируются по дате создания (новые первыми)

### 5.4. Онлайн пользователи

- Счетчик обновляется в реальном времени через WebSocket
- Показывает количество пользователей, подключенных к глобальному чату
- Обновляется при подключении/отключении пользователей

---

## 6. Важные замечания

1. **Авторизация:**
   - Все эндпоинты требуют JWT токен
   - WebSocket также требует токен в query параметре

2. **Файлы:**
   - Максимальный размер: 50 MB
   - Файлы сохраняются в `uploads/global_chat/{type}/`
   - Поддерживаются: изображения, видео, аудио, документы

3. **Блокировка:**
   - Блокировка работает односторонне (A блокирует B, B не видит сообщения A)
   - Заблокированный пользователь не уведомляется

4. **Удаление истории:**
   - Персональное удаление не удаляет сообщения из БД, только скрывает для пользователя
   - Удаление сообщения автором удаляет его для всех

5. **Производительность:**
   - WebSocket соединения хранятся в памяти
   - При перезапуске сервера соединения теряются
   - Рекомендуется использовать Redis для масштабирования

---

## 7. Дополнительные возможности (будущее)

1. **Реакции на сообщения:**
   - Лайки, эмодзи-реакции

2. **Ответы на сообщения:**
   - Цитирование сообщений

3. **Упоминания:**
   - @username для упоминания пользователей

4. **Модерация:**
   - Возможность администраторам удалять сообщения
   - Бан пользователей

5. **Статистика:**
   - Количество сообщений пользователя
   - Активность в чате

