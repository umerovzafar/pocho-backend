# Техническое задание: Система технической поддержки

## Общее описание

Система технической поддержки с чатом между пользователями и администраторами в реальном времени через WebSocket. Каждый пользователь может создать тикет поддержки, администраторы могут отвечать и управлять тикетами.

---

## 1. Архитектура системы

### 1.1. Модели базы данных

**Таблица `support_tickets`:**
- `id` - первичный ключ
- `user_id` - ID пользователя, создавшего тикет
- `subject` - тема/заголовок тикета
- `status` - статус (open, in_progress, waiting_for_user, resolved, closed)
- `priority` - приоритет (low, medium, high, urgent)
- `assigned_to` - ID администратора, назначенного на тикет
- `is_read_by_user` - прочитан ли тикет пользователем
- `is_read_by_admin` - прочитан ли тикет администратором
- `created_at` - дата создания
- `updated_at` - дата обновления
- `resolved_at` - дата решения
- `closed_at` - дата закрытия

**Таблица `support_messages`:**
- `id` - первичный ключ
- `ticket_id` - ID тикета
- `user_id` - ID пользователя (отправителя сообщения)
- `message` - текст сообщения
- `is_from_user` - True если от пользователя, False если от администратора
- `attachments` - JSON массив URL прикрепленных файлов
- `created_at` - дата создания

### 1.2. Статусы тикета

- **OPEN** - Открыт (новый тикет)
- **IN_PROGRESS** - В работе (администратор отвечает)
- **WAITING_FOR_USER** - Ожидание ответа пользователя
- **RESOLVED** - Решен
- **CLOSED** - Закрыт

### 1.3. Приоритеты тикета

- **LOW** - Низкий
- **MEDIUM** - Средний
- **HIGH** - Высокий
- **URGENT** - Срочный

---

## 2. Эндпоинты для пользователей

### 2.1. Создание тикета

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/support`

**Тело запроса:**
```json
{
  "subject": "Проблема с оплатой",
  "message": "Не могу пополнить баланс через карту"
}
```

**Ответ:**
```json
{
  "id": 1,
  "user_id": 123,
  "subject": "Проблема с оплатой",
  "status": "open",
  "priority": "medium",
  "assigned_to": null,
  "is_read_by_user": true,
  "is_read_by_admin": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": null,
  "resolved_at": null,
  "closed_at": null
}
```

### 2.2. Получение списка тикетов

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/support`

**Query параметры:**
- `skip` (int, default: 0) - количество пропущенных записей
- `limit` (int, default: 100) - максимальное количество записей
- `status` (optional) - фильтр по статусу (open, in_progress, resolved, closed)

**Ответ:**
```json
{
  "tickets": [
    {
      "id": 1,
      "user_id": 123,
      "subject": "Проблема с оплатой",
      "status": "open",
      "priority": "medium",
      "assigned_to": null,
      "is_read_by_user": true,
      "is_read_by_admin": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": null,
      "resolved_at": null,
      "closed_at": null
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

### 2.3. Получение тикета с сообщениями

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/{ticket_id}`

**Ответ:**
```json
{
  "id": 1,
  "user_id": 123,
  "subject": "Проблема с оплатой",
  "status": "in_progress",
  "priority": "medium",
  "assigned_to": 5,
  "is_read_by_user": true,
  "is_read_by_admin": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z",
  "resolved_at": null,
  "closed_at": null,
  "messages": [
    {
      "id": 1,
      "ticket_id": 1,
      "user_id": 123,
      "message": "Не могу пополнить баланс через карту",
      "is_from_user": true,
      "attachments": null,
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "ticket_id": 1,
      "user_id": 5,
      "message": "Здравствуйте! Проверяю вашу проблему.",
      "is_from_user": false,
      "attachments": null,
      "created_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

### 2.4. Отправка сообщения

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/{ticket_id}/messages`

**Тело запроса:**
```json
{
  "message": "Спасибо, жду ответа",
  "attachments": ["http://localhost:8000/uploads/screenshot.jpg"]
}
```

**Ответ:**
```json
{
  "id": 3,
  "ticket_id": 1,
  "user_id": 123,
  "message": "Спасибо, жду ответа",
  "is_from_user": true,
  "attachments": ["http://localhost:8000/uploads/screenshot.jpg"],
  "created_at": "2024-01-15T11:15:00Z"
}
```

### 2.5. Отметить тикет как прочитанный

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/{ticket_id}/read`

**Ответ:**
```json
{
  "success": true,
  "message": "Тикет отмечен как прочитанный"
}
```

---

## 3. Эндпоинты для администраторов

### 3.1. Получение всех тикетов

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/tickets`

**Query параметры:**
- `skip` (int, default: 0)
- `limit` (int, default: 100)
- `status` (optional) - фильтр по статусу
- `assigned_to` (optional) - ID администратора (0 для неназначенных)
- `user_id` (optional) - фильтр по ID пользователя

### 3.2. Получение тикета с сообщениями

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/tickets/{ticket_id}`

### 3.3. Отправка сообщения администратором

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/tickets/{ticket_id}/messages`

**Тело запроса:**
```json
{
  "message": "Проблема решена. Попробуйте снова.",
  "attachments": null
}
```

### 3.4. Обновление тикета

**Метод:** `PATCH`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/tickets/{ticket_id}`

**Тело запроса:**
```json
{
  "status": "resolved",
  "priority": "high",
  "assigned_to": 5
}
```

### 3.5. Отметить тикет как прочитанный (админ)

**Метод:** `POST`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/tickets/{ticket_id}/read`

### 3.6. Статистика тикетов

**Метод:** `GET`  
**Путь:** `http://127.0.0.1:8000/api/v1/support/admin/stats`

**Ответ:**
```json
{
  "total": 50,
  "open": 10,
  "in_progress": 5,
  "resolved": 30,
  "closed": 5
}
```

---

## 4. WebSocket для чата в реальном времени

### 4.1. Подключение к чату тикета

**WebSocket URL:** `ws://127.0.0.1:8000/api/v1/support/ws/ticket/{ticket_id}?token=<jwt_token>`

**После подключения:**
```json
{
  "type": "connection",
  "status": "connected",
  "ticket_id": 1,
  "user_id": 123,
  "is_admin": false
}
```

### 4.2. Получение нового сообщения

**Формат:**
```json
{
  "type": "new_message",
  "message": {
    "id": 3,
    "ticket_id": 1,
    "user_id": 123,
    "message": "Текст сообщения",
    "is_from_user": true,
    "attachments": null,
    "created_at": "2024-01-15T11:15:00Z"
  }
}
```

### 4.3. Поддержание соединения

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

## 5. Логика работы

### 5.1. Создание тикета

1. Пользователь создает тикет с первым сообщением
2. Статус автоматически устанавливается в `OPEN`
3. Администраторы получают уведомление через WebSocket

### 5.2. Отправка сообщения

**Пользователь:**
- Если тикет был закрыт/решен, он автоматически открывается заново
- Статус тикета обновляется на `OPEN` (если был закрыт)
- Тикет помечается как непрочитанный для администратора

**Администратор:**
- Если тикет был открыт, статус меняется на `IN_PROGRESS`
- Тикет помечается как непрочитанный для пользователя

### 5.3. Обновление статуса (администратор)

- При установке статуса `RESOLVED` автоматически устанавливается `resolved_at`
- При установке статуса `CLOSED` автоматически устанавливается `closed_at`
- Администратор может назначить тикет себе через `assigned_to`

---

## 6. Примеры использования

### 6.1. Создание тикета (curl)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Проблема с оплатой",
    "message": "Не могу пополнить баланс"
  }'
```

### 6.2. Отправка сообщения (curl)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/support/1/messages" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Дополнительная информация",
    "attachments": ["http://localhost:8000/uploads/screenshot.jpg"]
  }'
```

### 6.3. WebSocket подключение (JavaScript)

```javascript
const token = "YOUR_JWT_TOKEN";
const ticketId = 1;
const ws = new WebSocket(
  `ws://127.0.0.1:8000/api/v1/support/ws/ticket/${ticketId}?token=${token}`
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === "new_message") {
    console.log("Новое сообщение:", data.message);
    // Добавить сообщение в UI
  } else if (data.type === "connection") {
    console.log("Подключено к чату");
  }
};

// Отправка сообщения через REST API
async function sendMessage(ticketId, message) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/support/${ticketId}/messages`,
    {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    }
  );
  return await response.json();
}
```

### 6.4. Flutter пример

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class SupportChatService {
  WebSocketChannel? _channel;
  final String token;
  final int ticketId;
  
  SupportChatService(this.token, this.ticketId);
  
  void connect() {
    final uri = Uri.parse(
      'ws://127.0.0.1:8000/api/v1/support/ws/ticket/$ticketId?token=$token'
    );
    _channel = WebSocketChannel.connect(uri);
    
    _channel!.stream.listen(
      (message) {
        final data = jsonDecode(message);
        if (data['type'] == 'new_message') {
          _handleNewMessage(data['message']);
        }
      },
    );
    
    // Ping каждые 30 секунд
    Timer.periodic(Duration(seconds: 30), (_) {
      _channel?.sink.add('ping');
    });
  }
  
  void _handleNewMessage(Map<String, dynamic> message) {
    // Обновить UI с новым сообщением
  }
  
  Future<void> sendMessage(String text) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/v1/support/$ticketId/messages'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'message': text}),
    );
    // Сообщение будет доставлено через WebSocket всем участникам
  }
  
  void disconnect() {
    _channel?.sink.close();
  }
}
```

---

## 7. Важные замечания

1. **Авторизация:**
   - Все эндпоинты требуют JWT токен
   - Пользователи могут видеть только свои тикеты
   - Администраторы могут видеть все тикеты

2. **WebSocket:**
   - Требует JWT токен в query параметре
   - Автоматически закрывается при потере соединения
   - Отправляйте ping для поддержания соединения

3. **Статусы:**
   - Тикет автоматически открывается, если пользователь отвечает на закрытый/решенный тикет
   - Тикет автоматически переходит в `IN_PROGRESS` при первом ответе администратора

4. **Производительность:**
   - WebSocket соединения хранятся в памяти
   - При перезапуске сервера соединения теряются
   - Рекомендуется использовать Redis для масштабирования

5. **Файлы:**
   - Прикрепленные файлы должны быть загружены через отдельный эндпоинт загрузки
   - В `attachments` передается массив URL файлов

---

## 8. Дополнительные возможности (будущее)

1. **Категории тикетов:**
   - Разделение тикетов по категориям (технические, оплата, общие вопросы)

2. **Теги:**
   - Возможность добавлять теги к тикетам

3. **Внутренние заметки:**
   - Администраторы могут оставлять заметки, видимые только другим администраторам

4. **Автоматические ответы:**
   - Бот для первичной обработки тикетов

5. **Эскалация:**
   - Автоматическое повышение приоритета при долгом ожидании ответа





