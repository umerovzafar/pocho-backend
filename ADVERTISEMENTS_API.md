# API для управления рекламными блоками

## Описание

Система управления рекламными блоками с поддержкой:
- Создания и управления рекламой администраторами
- Отслеживания просмотров и кликов
- Фильтрации по позициям в приложении
- Статистики по эффективности рекламы
- Временных рамок показа рекламы
- Целевой аудитории

## Модели данных

### Advertisement (Реклама)

#### Поля для создания/обновления (AdvertisementCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `title` | string | ✅ Да | Заголовок рекламы (1-255 символов) | "Бесплатная мойка при заправке" |
| `description` | string | ❌ Нет | Описание/текст рекламы | "При заправке от 50 литров" |
| `image_url` | string | ✅ Да | URL изображения рекламы | "http://localhost:8000/uploads/advertisements/abc123.jpg" |
| `link_url` | string | ❌ Нет | URL для перехода при клике | "https://example.com/promo" |
| `link_type` | string | ❌ Нет | Тип ссылки: `internal`, `external`, `deep_link` | "internal" |
| `ad_type` | enum | ❌ Нет | Тип рекламного блока (по умолчанию `banner`) | "banner" |
| `position` | enum | ❌ Нет | Позиция в приложении (по умолчанию `home_top`) | "home_top" |
| `status` | enum | ❌ Нет | Статус рекламы (по умолчанию `active`) | "active" |
| `is_active` | boolean | ❌ Нет | Активна ли реклама (по умолчанию true) | true |
| `start_date` | datetime | ❌ Нет | Дата начала показа (ISO 8601) | "2026-01-06T00:00:00Z" |
| `end_date` | datetime | ❌ Нет | Дата окончания показа (ISO 8601) | "2026-01-13T23:59:59Z" |
| `priority` | integer | ❌ Нет | Приоритет показа (больше = выше, по умолчанию 0) | 10 |
| `display_order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |
| `target_audience` | string | ❌ Нет | Целевая аудитория (`all`, `premium`, `new_users`) | "all" |
| `show_conditions` | string | ❌ Нет | JSON с условиями показа | `{"min_app_version": "1.0.0"}` |

#### Поля в ответе (AdvertisementResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор рекламы | 1 |
| `title` | string | Заголовок рекламы | "Бесплатная мойка при заправке" |
| `description` | string \| null | Описание/текст рекламы | "При заправке от 50 литров" |
| `image_url` | string | URL изображения рекламы | "http://localhost:8000/uploads/advertisements/abc123.jpg" |
| `link_url` | string \| null | URL для перехода при клике | "https://example.com/promo" |
| `link_type` | string \| null | Тип ссылки | "internal" |
| `ad_type` | string | Тип рекламного блока | "banner" |
| `position` | string | Позиция в приложении | "home_top" |
| `status` | string | Статус рекламы | "active" |
| `is_active` | boolean | Активна ли реклама | true |
| `start_date` | datetime \| null | Дата начала показа | "2026-01-06T00:00:00Z" |
| `end_date` | datetime \| null | Дата окончания показа | "2026-01-13T23:59:59Z" |
| `priority` | integer | Приоритет показа | 10 |
| `display_order` | integer | Порядок отображения | 0 |
| `target_audience` | string \| null | Целевая аудитория | "all" |
| `show_conditions` | string \| null | JSON с условиями показа | `{"min_app_version": "1.0.0"}` |
| `views_count` | integer | Количество просмотров (автоматически обновляется) | 1250 |
| `clicks_count` | integer | Количество кликов (автоматически обновляется) | 87 |
| `created_by_admin_id` | integer | ID администратора, создавшего рекламу | 1 |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T10:15:30.123Z" |

### AdvertisementView (Просмотр рекламы)

#### Поля в ответе (AdvertisementViewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор просмотра | 1 |
| `advertisement_id` | integer | ID рекламы | 1 |
| `user_id` | integer \| null | ID пользователя (если авторизован) | 5 |
| `ip_address` | string \| null | IP адрес | "192.168.1.1" |
| `user_agent` | string \| null | User-Agent браузера/приложения | "Mozilla/5.0..." |
| `device_type` | string \| null | Тип устройства (`mobile`, `tablet`, `desktop`) | "mobile" |
| `app_version` | string \| null | Версия приложения | "1.2.3" |
| `viewed_at` | datetime | Дата и время просмотра (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### AdvertisementClick (Клик по рекламе)

#### Поля в ответе (AdvertisementClickResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор клика | 1 |
| `advertisement_id` | integer | ID рекламы | 1 |
| `user_id` | integer \| null | ID пользователя (если авторизован) | 5 |
| `ip_address` | string \| null | IP адрес | "192.168.1.1" |
| `user_agent` | string \| null | User-Agent браузера/приложения | "Mozilla/5.0..." |
| `device_type` | string \| null | Тип устройства | "mobile" |
| `clicked_at` | datetime | Дата и время клика (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Типы рекламных блоков

| Тип | Описание |
|-----|----------|
| `banner` | Баннер (горизонтальный или вертикальный) |
| `promo` | Промо-акция (специальное предложение) |
| `notification` | Уведомление |
| `popup` | Всплывающее окно |
| `card` | Карточка рекламы |

## Позиции в приложении

| Позиция | Описание |
|---------|----------|
| `home_top` | Верх главной страницы |
| `home_bottom` | Низ главной страницы |
| `gas_stations_list` | В списке заправок |
| `restaurants_list` | В списке ресторанов |
| `service_stations_list` | В списке СТО |
| `car_washes_list` | В списке автомоек |
| `profile` | На странице профиля |
| `global_chat` | В глобальном чате |
| `other` | Другое |

## Статусы рекламы

| Статус | Описание | Видимость для клиентов |
|--------|----------|------------------------|
| `active` | Активна | ✅ Видна (если соответствует условиям) |
| `inactive` | Неактивна | ❌ Не видна |
| `archived` | Архивирована | ❌ Не видна |

## Клиентские эндпоинты

### GET /api/v1/advertisements/
Получение активных рекламных блоков для определенной позиции

**Требуется авторизация:** ❌ Нет (опционально, для целевой аудитории)

**Параметры запроса:**
- `position` (обязательный, enum) - Позиция рекламы в приложении (см. Позиции в приложении)

**Пример:**
```
GET /api/v1/advertisements/?position=home_top
```

**Ответ (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Бесплатная мойка при заправке",
    "description": "При заправке от 50 литров",
    "image_url": "http://localhost:8000/uploads/advertisements/abc123.jpg",
    "link_url": "https://example.com/promo",
    "link_type": "internal",
    "ad_type": "banner",
    "position": "home_top",
    "priority": 10,
    "display_order": 0
  },
  {
    "id": 2,
    "title": "Скидка 10% на все виды топлива",
    "description": "До конца недели",
    "image_url": "http://localhost:8000/uploads/advertisements/def456.jpg",
    "link_url": null,
    "link_type": null,
    "ad_type": "promo",
    "position": "home_top",
    "priority": 5,
    "display_order": 1
  }
]
```

**Особенности:**
- Возвращаются только активные рекламы (`status=active`, `is_active=true`)
- Учитываются временные рамки (`start_date` и `end_date`)
- Сортировка по приоритету (убывание) и порядку отображения (возрастание)
- Если пользователь авторизован, учитывается целевая аудитория

### POST /api/v1/advertisements/{advertisement_id}/view
Регистрация просмотра рекламы

**Требуется авторизация:** ❌ Нет (опционально)

**Параметры пути:**
- `advertisement_id` (integer, обязательный) - ID рекламы

**Параметры запроса (query, все опциональны):**
- `ip_address` - IP адрес (если не указан, берется из запроса)
- `user_agent` - User-Agent (если не указан, берется из заголовков)
- `device_type` - Тип устройства (`mobile`, `tablet`, `desktop`)
- `app_version` - Версия приложения

**Пример:**
```
POST /api/v1/advertisements/1/view?device_type=mobile&app_version=1.2.3
```

**Ответ (201 Created):**
```json
{
  "message": "Просмотр зарегистрирован",
  "advertisement_id": 1
}
```

**Особенности:**
- Автоматически увеличивает счетчик `views_count` рекламы
- Сохраняет информацию о просмотре для аналитики
- Если пользователь авторизован, сохраняется `user_id`

### POST /api/v1/advertisements/{advertisement_id}/click
Регистрация клика по рекламе

**Требуется авторизация:** ❌ Нет (опционально)

**Параметры пути:**
- `advertisement_id` (integer, обязательный) - ID рекламы

**Параметры запроса (query, все опциональны):**
- `ip_address` - IP адрес (если не указан, берется из запроса)
- `user_agent` - User-Agent (если не указан, берется из заголовков)
- `device_type` - Тип устройства (`mobile`, `tablet`, `desktop`)

**Пример:**
```
POST /api/v1/advertisements/1/click?device_type=mobile
```

**Ответ (201 Created):**
```json
{
  "message": "Клик зарегистрирован",
  "advertisement_id": 1
}
```

**Особенности:**
- Автоматически увеличивает счетчик `clicks_count` рекламы
- Сохраняет информацию о клике для аналитики
- Если пользователь авторизован, сохраняется `user_id`

## Администраторские эндпоинты

### POST /api/v1/admin/advertisements/
Создание новой рекламы

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "title": "Бесплатная мойка при заправке",
  "description": "При заправке от 50 литров",
  "image_url": "http://localhost:8000/uploads/advertisements/abc123.jpg",
  "link_url": "https://example.com/promo",
  "link_type": "internal",
  "ad_type": "banner",
  "position": "home_top",
  "status": "active",
  "is_active": true,
  "start_date": "2026-01-06T00:00:00Z",
  "end_date": "2026-01-13T23:59:59Z",
  "priority": 10,
  "display_order": 0,
  "target_audience": "all"
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "title": "Бесплатная мойка при заправке",
  "description": "При заправке от 50 литров",
  "image_url": "http://localhost:8000/uploads/advertisements/abc123.jpg",
  "link_url": "https://example.com/promo",
  "link_type": "internal",
  "ad_type": "banner",
  "position": "home_top",
  "status": "active",
  "is_active": true,
  "start_date": "2026-01-06T00:00:00Z",
  "end_date": "2026-01-13T23:59:59Z",
  "priority": 10,
  "display_order": 0,
  "target_audience": "all",
  "show_conditions": null,
  "views_count": 0,
  "clicks_count": 0,
  "created_by_admin_id": 1,
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": null
}
```

### POST /api/v1/admin/advertisements/upload-image
Загрузка изображения для рекламы

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения (разрешены: image/jpeg, image/jpg, image/png, image/webp, максимум 5MB)

**Ответ (201 Created):**
```json
{
  "image_url": "http://localhost:8000/uploads/advertisements/abc123.jpg"
}
```

### GET /api/v1/admin/advertisements/
Получение списка всех реклам

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)
- `ad_type` - Фильтр по типу рекламы
- `position` - Фильтр по позиции
- `status` - Фильтр по статусу
- `is_active` - Фильтр по активности (true/false)
- `target_audience` - Фильтр по целевой аудитории
- `search_query` - Поиск по названию или описанию

**Ответ:**
```json
{
  "advertisements": [...],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

### GET /api/v1/admin/advertisements/{advertisement_id}
Получение детальной информации о рекламе

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Ответ:** `AdvertisementDetailResponse` (включает последние просмотры и клики)

### PUT /api/v1/admin/advertisements/{advertisement_id}
Обновление рекламы

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Запрос:** `AdvertisementUpdate` (все поля опциональны)

### DELETE /api/v1/admin/advertisements/{advertisement_id}
Удаление рекламы

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Ответ (204 No Content):** Пустое тело ответа

### GET /api/v1/admin/advertisements/{advertisement_id}/statistics
Получение статистики по рекламе

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Ответ:**
```json
{
  "advertisement_id": 1,
  "title": "Бесплатная мойка при заправке",
  "views_count": 1250,
  "clicks_count": 87,
  "click_through_rate": 6.96,
  "unique_views": 890,
  "unique_clicks": 65,
  "views_today": 45,
  "clicks_today": 3,
  "views_this_week": 320,
  "clicks_this_week": 22,
  "views_this_month": 1250,
  "clicks_this_month": 87
}
```

**Поля статистики:**
- `views_count` - Общее количество просмотров
- `clicks_count` - Общее количество кликов
- `click_through_rate` - CTR в процентах (clicks/views * 100)
- `unique_views` - Уникальные просмотры (по пользователям)
- `unique_clicks` - Уникальные клики (по пользователям)
- `views_today` - Просмотры за сегодня
- `clicks_today` - Клики за сегодня
- `views_this_week` - Просмотры за эту неделю
- `clicks_this_week` - Клики за эту неделю
- `views_this_month` - Просмотры за этот месяц
- `clicks_this_month` - Клики за этот месяц

### GET /api/v1/admin/advertisements/{advertisement_id}/views
Получение просмотров рекламы

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)

**Ответ:** Список `AdvertisementViewResponse`

### GET /api/v1/admin/advertisements/{advertisement_id}/clicks
Получение кликов по рекламе

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)

**Ответ:** Список `AdvertisementClickResponse`

## Особенности

1. **Автоматическое отслеживание**: При регистрации просмотра или клика автоматически обновляются счетчики `views_count` и `clicks_count` в рекламе.

2. **Временные рамки**: Реклама показывается только если:
   - `status = active`
   - `is_active = true`
   - Текущая дата >= `start_date` (если указана)
   - Текущая дата <= `end_date` (если указана)

3. **Приоритет и порядок**: Рекламы сортируются сначала по приоритету (убывание), затем по порядку отображения (возрастание).

4. **Целевая аудитория**: Можно настроить показ рекламы для определенной аудитории (`all`, `premium`, `new_users` и т.д.).

5. **Условия показа**: Можно указать JSON с дополнительными условиями показа (например, минимальная версия приложения).

6. **Статистика**: Система автоматически собирает статистику по просмотрам и кликам, включая уникальные просмотры/клики и статистику за разные периоды.

## Примеры использования

### Создание рекламы
```bash
curl -X POST "http://localhost:8000/api/v1/admin/advertisements/" \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Бесплатная мойка при заправке",
    "description": "При заправке от 50 литров",
    "image_url": "http://localhost:8000/uploads/advertisements/abc123.jpg",
    "link_url": "https://example.com/promo",
    "ad_type": "banner",
    "position": "home_top",
    "priority": 10,
    "start_date": "2026-01-06T00:00:00Z",
    "end_date": "2026-01-13T23:59:59Z"
  }'
```

### Получение рекламы для клиента
```bash
curl -X GET "http://localhost:8000/api/v1/advertisements/?position=home_top" \
  -H "Authorization: Bearer <token>"  # Опционально
```

### Регистрация просмотра
```bash
curl -X POST "http://localhost:8000/api/v1/advertisements/1/view?device_type=mobile&app_version=1.2.3" \
  -H "Authorization: Bearer <token>"  # Опционально
```

### Регистрация клика
```bash
curl -X POST "http://localhost:8000/api/v1/advertisements/1/click?device_type=mobile" \
  -H "Authorization: Bearer <token>"  # Опционально
```

### Получение статистики
```bash
curl -X GET "http://localhost:8000/api/v1/admin/advertisements/1/statistics" \
  -H "Authorization: Bearer <admin_token>"
```

## Ограничения

- Максимальный размер файла изображения: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка реклам в одном запросе: 1000 записей
- Приоритет: целое число (больше = выше приоритет)



