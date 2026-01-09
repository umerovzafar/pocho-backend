# Техническое задание: Система уведомлений

## Общее описание

Система уведомлений с использованием WebSocket для доставки уведомлений в реальном времени. Поддерживает два типа уведомлений: персональные (для конкретного пользователя) и глобальные (для всех пользователей).

---

## 1. Техническое задание для мобильной версии (Flutter)

### 1.1. WebSocket подключение

**Эндпоинт:** `ws://127.0.0.1:8000/api/v1/notifications/ws/notifications?token=<jwt_token>`

**Протокол подключения:**
1. Подключиться к WebSocket с JWT токеном в query параметре `token`
2. После успешного подключения получить сообщение:
   ```json
   {
     "type": "connection",
     "status": "connected",
     "user_id": 123,
     "message": "Подключено к системе уведомлений"
   }
   ```
3. Поддерживать соединение, отправляя `"ping"` для поддержания активности
4. Получать ответ `{"type": "pong"}` на ping

**Формат входящих уведомлений:**
```json
{
  "type": "notification",
  "notification": {
    "id": 1,
    "user_id": 123,
    "title": "Новое уведомление",
    "message": "Текст уведомления",
    "notification_type": "info",
    "is_read": false,
    "read_at": null,
    "extra_data": {
      "action_url": "/some/path",
      "image_url": "http://..."
    },
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### 1.2. Push-уведомления

**Требования:**
1. При получении уведомления через WebSocket:
   - Если приложение открыто - показать уведомление в UI
   - Если приложение в фоне - отправить push-уведомление через FCM (Firebase Cloud Messaging)

2. При открытии приложения:
   - Подключиться к WebSocket
   - Загрузить непрочитанные уведомления через REST API
   - Показать badge с количеством непрочитанных

3. При получении уведомления:
   - Сохранить в локальную базу данных (SQLite/Hive)
   - Показать системное уведомление (если приложение в фоне)
   - Обновить счетчик непрочитанных

### 1.3. REST API эндпоинты

**Получение списка уведомлений:**
```
GET /api/v1/notifications
Headers: Authorization: Bearer <token>
Query params:
  - skip: int (default: 0)
  - limit: int (default: 100, max: 1000)
  - unread_only: bool (optional)
```

**Ответ:**
```json
{
  "notifications": [
    {
      "id": 1,
      "user_id": 123,
      "title": "Заголовок",
      "message": "Текст",
      "notification_type": "info",
      "is_read": false,
      "read_at": null,
      "extra_data": {},
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 50,
  "unread_count": 10,
  "skip": 0,
  "limit": 100
}
```

**Получение статистики:**
```
GET /api/v1/notifications/stats
Headers: Authorization: Bearer <token>
```

**Ответ:**
```json
{
  "total": 50,
  "unread": 10,
  "read": 40
}
```

**Отметить как прочитанное:**
```
PATCH /api/v1/notifications/{notification_id}/read
Headers: Authorization: Bearer <token>
```

**Отметить все как прочитанные:**
```
POST /api/v1/notifications/read-all
Headers: Authorization: Bearer <token>
```

**Удалить уведомление:**
```
DELETE /api/v1/notifications/{notification_id}
Headers: Authorization: Bearer <token>
```

**Ответ:**
```json
{
  "success": true,
  "message": "Уведомление удалено" // или "Глобальное уведомление скрыто"
  "notification_id": 1
}
```

**Примечание:**
- Персональные уведомления удаляются полностью из БД
- Глобальные уведомления скрываются для конкретного пользователя (не удаляются из БД, чтобы другие пользователи могли их видеть)

**Удалить все уведомления:**
```
DELETE /api/v1/notifications
Headers: Authorization: Bearer <token>
```

**Ответ:**
```json
{
  "success": true,
  "message": "Удалено 15 уведомлений",
  "count": 15
}
```

### 1.4. UI компоненты

**Экран уведомлений:**
- Список уведомлений с группировкой по дате
- Индикатор непрочитанных (красная точка или badge)
- Swipe-to-delete для удаления
- Pull-to-refresh для обновления
- Фильтр: Все / Непрочитанные

**Карточка уведомления:**
- Иконка типа уведомления (info, warning, success, error, promotion)
- Заголовок (жирный)
- Текст сообщения
- Время получения
- Индикатор прочитанности
- Действие при нажатии (если указано в `extra_data.action_url`)

**Badge на иконке уведомлений:**
- Показывать количество непрочитанных
- Обновлять при получении новых уведомлений
- Скрывать, если непрочитанных нет

### 1.5. Пример реализации (Flutter)

```dart
// WebSocket подключение
class NotificationWebSocket {
  WebSocketChannel? _channel;
  final String token;
  
  NotificationWebSocket(this.token);
  
  void connect() {
    final uri = Uri.parse(
      'ws://127.0.0.1:8000/api/v1/notifications/ws/notifications?token=$token'
    );
    _channel = WebSocketChannel.connect(uri);
    
    _channel!.stream.listen(
      (message) {
        final data = jsonDecode(message);
        if (data['type'] == 'notification') {
          _handleNotification(data['notification']);
        }
      },
      onError: (error) => print('WebSocket error: $error'),
      onDone: () => print('WebSocket closed'),
    );
    
    // Ping каждые 30 секунд
    Timer.periodic(Duration(seconds: 30), (_) {
      _channel?.sink.add('ping');
    });
  }
  
  void _handleNotification(Map<String, dynamic> notification) {
    // Сохранить в локальную БД
    // Показать системное уведомление
    // Обновить счетчик
  }
  
  void disconnect() {
    _channel?.sink.close();
  }
}

// REST API клиент
class NotificationService {
  final String baseUrl = 'http://127.0.0.1:8000';
  final String token;
  
  Future<NotificationListResponse> getNotifications({
    int skip = 0,
    int limit = 100,
    bool? unreadOnly,
  }) async {
    final uri = Uri.parse('$baseUrl/api/v1/notifications')
        .replace(queryParameters: {
      'skip': skip.toString(),
      'limit': limit.toString(),
      if (unreadOnly != null) 'unread_only': unreadOnly.toString(),
    });
    
    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );
    
    return NotificationListResponse.fromJson(jsonDecode(response.body));
  }
  
  Future<void> markAsRead(int notificationId) async {
    await http.patch(
      Uri.parse('$baseUrl/api/v1/notifications/$notificationId/read'),
      headers: {'Authorization': 'Bearer $token'},
    );
  }
  
  Future<void> markAllAsRead() async {
    await http.post(
      Uri.parse('$baseUrl/api/v1/notifications/read-all'),
      headers: {'Authorization': 'Bearer $token'},
    );
  }
}
```

### 1.6. Типы уведомлений и их отображение

| Тип | Иконка | Цвет | Описание |
|-----|--------|------|----------|
| `info` | info | Синий | Информационное сообщение |
| `warning` | warning | Желтый | Предупреждение |
| `success` | check_circle | Зеленый | Успешное действие |
| `error` | error | Красный | Ошибка |
| `promotion` | local_offer | Оранжевый | Акция/промо |

---

## 2. Техническое задание для панели администратора

### 2.1. Эндпоинты для создания уведомлений

**Создание уведомления:**
```
POST /api/v1/admin/notification
Headers: 
  Authorization: Bearer <admin_token>
  Content-Type: application/json
```

**Тело запроса (персональное уведомление):**
```json
{
  "user_id": 123,
  "title": "Ваш документ одобрен",
  "message": "Ваш паспорт успешно прошел верификацию",
  "notification_type": "success",
  "extra_data": {
    "action_url": "/profile/documents"
  }
}
```

**Тело запроса (глобальное уведомление):**
```json
{
  "user_id": null,
  "title": "Новая акция!",
  "message": "Скидка 20% на все заправки до конца месяца",
  "notification_type": "promotion",
  "extra_data": {
    "action_url": "/promotions",
    "image_url": "http://localhost:8000/images/promo.jpg"
  }
}
```

**Ответ:**
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Ваш документ одобрен",
  "message": "Ваш паспорт успешно прошел верификацию",
  "notification_type": "success",
  "is_read": false,
  "read_at": null,
  "extra_data": {
    "action_url": "/profile/documents"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Получение списка всех уведомлений:**
```
GET /api/v1/admin/notifications
Headers: Authorization: Bearer <admin_token>
Query params:
  - skip: int (default: 0)
  - limit: int (default: 100, max: 1000)
  - user_id: int (optional, фильтр по пользователю)
  - notification_type: string (optional, фильтр по типу)
```

### 2.2. UI панели администратора

**Форма создания уведомления:**

1. **Тип уведомления:**
   - Радио-кнопки: "Персональное" / "Глобальное"
   - Если выбрано "Персональное" - поле выбора пользователя (поиск по телефону/имени)

2. **Заголовок:**
   - Текстовое поле (обязательное, 1-200 символов)

3. **Текст сообщения:**
   - Многострочное текстовое поле (обязательное)

4. **Тип уведомления:**
   - Выпадающий список:
     - Информационное (info)
     - Предупреждение (warning)
     - Успех (success)
     - Ошибка (error)
     - Акция/Промо (promotion)

5. **Дополнительные данные (опционально):**
   - URL действия (`action_url`) - куда перейти при нажатии
   - URL изображения (`image_url`) - изображение для уведомления
   - Другие данные (JSON редактор)

6. **Кнопка "Отправить":**
   - Создает уведомление в БД
   - Отправляет через WebSocket всем подключенным пользователям
   - Показывает сообщение об успехе

**Список уведомлений:**
- Таблица со всеми уведомлениями
- Фильтры: по пользователю, по типу, по дате
- Поиск по тексту
- Статистика: всего уведомлений, персональных, глобальных

**Пример формы (HTML/React):**
```html
<form id="notification-form">
  <div>
    <label>Тип уведомления:</label>
    <input type="radio" name="type" value="personal" checked> Персональное
    <input type="radio" name="type" value="global"> Глобальное
  </div>
  
  <div id="user-selector" style="display: block;">
    <label>Пользователь:</label>
    <select name="user_id">
      <option value="">Выберите пользователя</option>
      <!-- Список пользователей -->
    </select>
  </div>
  
  <div>
    <label>Заголовок:</label>
    <input type="text" name="title" required maxlength="200">
  </div>
  
  <div>
    <label>Сообщение:</label>
    <textarea name="message" required></textarea>
  </div>
  
  <div>
    <label>Тип:</label>
    <select name="notification_type">
      <option value="info">Информационное</option>
      <option value="warning">Предупреждение</option>
      <option value="success">Успех</option>
      <option value="error">Ошибка</option>
      <option value="promotion">Акция/Промо</option>
    </select>
  </div>
  
  <div>
    <label>URL действия (опционально):</label>
    <input type="url" name="action_url">
  </div>
  
  <button type="submit">Отправить уведомление</button>
</form>
```

### 2.3. Пример использования (JavaScript)

```javascript
// Создание персонального уведомления
async function createPersonalNotification(userId, title, message, type = 'info') {
  const response = await fetch('http://127.0.0.1:8000/api/v1/admin/notification', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      title: title,
      message: message,
      notification_type: type,
      extra_data: {}
    })
  });
  
  return await response.json();
}

// Создание глобального уведомления
async function createGlobalNotification(title, message, type = 'info') {
  const response = await fetch('http://127.0.0.1:8000/api/v1/admin/notification', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: null,
      title: title,
      message: message,
      notification_type: type,
      extra_data: {}
    })
  });
  
  return await response.json();
}

// Получение списка уведомлений
async function getAllNotifications(skip = 0, limit = 100) {
  const response = await fetch(
    `http://127.0.0.1:8000/api/v1/admin/notifications?skip=${skip}&limit=${limit}`,
    {
      headers: {
        'Authorization': `Bearer ${adminToken}`
      }
    }
  );
  
  return await response.json();
}
```

---

## 3. Архитектура системы

### 3.1. База данных

**Таблица `notifications`:**
- `id` - первичный ключ
- `user_id` - ID пользователя (NULL для глобальных)
- `title` - заголовок
- `message` - текст сообщения
- `notification_type` - тип (info, warning, success, error, promotion)
- `is_read` - статус прочтения
- `read_at` - дата прочтения
- `extra_data` - дополнительные данные (JSON)
- `created_at` - дата создания

### 3.2. WebSocket соединения

**Менеджер соединений:**
- Хранит активные WebSocket соединения по `user_id`
- Отправляет персональные уведомления конкретному пользователю
- Отправляет глобальные уведомления всем подключенным пользователям
- Автоматически удаляет отключенные соединения

### 3.3. Поток данных

1. **Администратор создает уведомление:**
   - POST `/api/v1/admin/notification`
   - Сохранение в БД
   - Отправка через WebSocket всем подключенным пользователям

2. **Пользователь получает уведомление:**
   - Через WebSocket (если подключен)
   - При следующем запросе через REST API (если не подключен)

3. **Пользователь отмечает как прочитанное:**
   - PATCH `/api/v1/notifications/{id}/read`
   - Обновление в БД
   - Обновление UI

---

## 4. Примеры использования

### 4.1. Создание персонального уведомления (администратор)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/notification" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "title": "Документ одобрен",
    "message": "Ваш паспорт успешно прошел верификацию",
    "notification_type": "success",
    "extra_data": {
      "action_url": "/profile/documents"
    }
  }'
```

### 4.2. Создание глобального уведомления (администратор)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/notification" \
  -H "Authorization: Bearer ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": null,
    "title": "Новая акция!",
    "message": "Скидка 20% на все заправки",
    "notification_type": "promotion",
    "extra_data": {
      "action_url": "/promotions",
      "image_url": "http://localhost:8000/images/promo.jpg"
    }
  }'
```

### 4.3. Получение уведомлений (пользователь)

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/notifications?unread_only=true" \
  -H "Authorization: Bearer USER_TOKEN"
```

### 4.4. Отметить как прочитанное (пользователь)

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/notifications/1/read" \
  -H "Authorization: Bearer USER_TOKEN"
```

### 4.5. Удалить уведомление (пользователь)

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/notifications/1" \
  -H "Authorization: Bearer USER_TOKEN"
```

### 4.6. Удалить все уведомления (пользователь)

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/notifications" \
  -H "Authorization: Bearer USER_TOKEN"
```

### 4.7. Удалить уведомление (администратор)

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/admin/notification/1" \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

**Примечание:** Администратор может удалять любые уведомления (персональные и глобальные), они полностью удаляются из БД.

---

## 5. Важные замечания

1. **WebSocket подключение:**
   - Требует JWT токен в query параметре
   - Автоматически переподключается при разрыве соединения
   - Отправляет ping каждые 30 секунд для поддержания соединения

2. **Глобальные уведомления:**
   - Отправляются всем подключенным пользователям
   - Сохраняются в БД с `user_id = NULL`
   - Каждый пользователь видит их в своем списке

3. **Персональные уведомления:**
   - Отправляются только указанному пользователю
   - Сохраняются в БД с `user_id = <user_id>`
   - Видны только этому пользователю

4. **Статус прочтения:**
   - По умолчанию `is_read = false`
   - Обновляется при вызове эндпоинта `/read`
   - Глобальные уведомления имеют отдельный статус для каждого пользователя через `NotificationReadStatus`

5. **Удаление уведомлений:**
   - **Персональные уведомления**: удаляются полностью из БД при удалении пользователем
   - **Глобальные уведомления**: скрываются для конкретного пользователя через `NotificationReadStatus.is_deleted`, но остаются в БД для других пользователей
   - **Администратор**: может удалять любые уведомления полностью из БД через эндпоинт `/api/v1/admin/notification/{id}`

6. **Производительность:**
   - WebSocket соединения хранятся в памяти
   - При перезапуске сервера соединения теряются
   - Рекомендуется использовать Redis для масштабирования

---

## 6. Дополнительные возможности (будущее)

1. **Групповые уведомления:**
   - Отправка уведомления группе пользователей (по уровню, по региону, etc.)

2. **Расписание уведомлений:**
   - Отложенная отправка уведомлений
   - Периодические уведомления

3. **Шаблоны уведомлений:**
   - Предустановленные шаблоны для часто используемых уведомлений

4. **Статистика:**
   - Процент прочитанных уведомлений
   - Время до прочтения
   - Эффективность уведомлений

