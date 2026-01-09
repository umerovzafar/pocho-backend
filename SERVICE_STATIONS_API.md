# API для станций технического обслуживания (СТО)

## Описание

Система управления станциями технического обслуживания с поддержкой:
- Добавления СТО (пользователями и админами)
- Управления ценами на услуги
- Загрузки фотографий
- Отзывов и рейтингов
- Фильтрации по различным параметрам
- Поиска по близости

## Модели данных

### ServiceStation (СТО)

#### Поля для создания/обновления (ServiceStationCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название СТО (1-255 символов) | "Автосервис ПоЧо" |
| `address` | string | ✅ Да | Полный адрес СТО (минимум 1 символ) | "Амира Темура, 15, Tashkent" |
| `latitude` | float | ✅ Да | Широта в градусах (-90 до 90) | 41.3111 |
| `longitude` | float | ✅ Да | Долгота в градусах (-180 до 180) | 69.2797 |
| `phone` | string | ❌ Нет | Номер телефона | "+998 90 123 45 67" |
| `email` | string | ❌ Нет | Email адрес | "info@service.uz" |
| `website` | string | ❌ Нет | Сайт СТО | "https://service.uz" |
| `is_24_7` | boolean | ❌ Нет | Работает ли СТО круглосуточно (по умолчанию false) | false |
| `working_hours` | string | ❌ Нет | Режим работы (если не 24/7) | "08:00-20:00" |
| `description` | string | ❌ Нет | Описание СТО | "Полный спектр услуг по ремонту автомобилей" |
| `has_parking` | boolean | ❌ Нет | Есть ли парковка (по умолчанию false) | true |
| `has_waiting_room` | boolean | ❌ Нет | Есть ли комната ожидания (по умолчанию false) | true |
| `has_cafe` | boolean | ❌ Нет | Есть ли кафе (по умолчанию false) | false |
| `accepts_cards` | boolean | ❌ Нет | Принимает ли карты (по умолчанию false) | true |
| `category` | string | ❌ Нет | Категория СТО (по умолчанию "СТО") | "СТО" |
| `service_prices` | array | ❌ Нет | Массив цен на услуги (см. ServicePriceCreate) | см. ниже |

#### Поля в ответе (ServiceStationResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор СТО | 1 |
| `name` | string | Название СТО | "Автосервис ПоЧо" |
| `address` | string | Полный адрес СТО | "Амира Темура, 15, Tashkent" |
| `latitude` | float | Широта в градусах | 41.3111 |
| `longitude` | float | Долгота в градусах | 69.2797 |
| `phone` | string \| null | Номер телефона | "+998 90 123 45 67" |
| `email` | string \| null | Email адрес | "info@service.uz" |
| `website` | string \| null | Сайт СТО | "https://service.uz" |
| `is_24_7` | boolean | Работает ли СТО круглосуточно | false |
| `working_hours` | string \| null | Режим работы | "08:00-20:00" |
| `description` | string \| null | Описание СТО | "Полный спектр услуг..." |
| `has_parking` | boolean | Есть ли парковка | true |
| `has_waiting_room` | boolean | Есть ли комната ожидания | true |
| `has_cafe` | boolean | Есть ли кафе | false |
| `accepts_cards` | boolean | Принимает ли карты | true |
| `category` | string | Категория СТО | "СТО" |
| `rating` | float | Средний рейтинг (0.0-5.0), автоматически рассчитывается | 4.8 |
| `reviews_count` | integer | Количество отзывов, автоматически обновляется | 127 |
| `status` | string | Статус СТО: `pending`, `approved`, `rejected`, `archived` | "approved" |
| `has_promotions` | boolean | Есть ли акции/промо-предложения | true |
| `service_prices` | array | Массив цен на услуги (см. ServicePriceResponse) | см. ниже |
| `photos` | array | Массив фотографий СТО (см. ServiceStationPhotoResponse) | см. ниже |
| `main_photo` | string \| null | URL главной фотографии СТО | "http://localhost:8000/uploads/service_stations/1_abc123.jpg" |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ServicePrice (Цена на услугу)

#### Поля для создания/обновления (ServicePriceCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `service_type` | string | ✅ Да | Тип услуги (см. Типы услуг) | "Замена масла" |
| `service_name` | string | ❌ Нет | Название конкретной услуги (до 255 символов) | "Замена масла двигателя" |
| `price` | float | ✅ Да | Цена в сумах (должна быть больше 0) | 150000.0 |
| `description` | string | ❌ Нет | Описание услуги | "Замена моторного масла с фильтром" |

#### Поля в ответе (ServicePriceResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор цены | 1 |
| `service_station_id` | integer | ID СТО | 1 |
| `service_type` | string | Тип услуги | "Замена масла" |
| `service_name` | string \| null | Название конкретной услуги | "Замена масла двигателя" |
| `price` | float | Цена в сумах | 150000.0 |
| `description` | string \| null | Описание услуги | "Замена моторного масла с фильтром" |
| `updated_at` | datetime \| null | Дата и время последнего обновления цены (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ServiceStationPhoto (Фотография)

#### Поля для создания (ServiceStationPhotoCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `is_main` | boolean | ❌ Нет | Является ли фотография главной (по умолчанию false) | true |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

**Примечание:** Файл загружается через `multipart/form-data` с полем `file`.

#### Поля в ответе (ServiceStationPhotoResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор фотографии | 1 |
| `service_station_id` | integer | ID СТО | 1 |
| `photo_url` | string | Полный URL фотографии | "http://localhost:8000/uploads/service_stations/1_abc123.jpg" |
| `is_main` | boolean | Является ли фотография главной | true |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время загрузки (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ServiceStationReview (Отзыв)

#### Поля для создания/обновления (ServiceStationReviewCreate/ServiceStationReviewUpdate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `rating` | integer | ✅ Да | Рейтинг от 1 до 5 | 5 |
| `comment` | string | ❌ Нет | Текст отзыва | "Отличный сервис! Быстро и качественно." |

#### Поля в ответе (ServiceStationReviewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор отзыва | 1 |
| `service_station_id` | integer | ID СТО | 1 |
| `user_id` | integer | ID пользователя, оставившего отзыв | 5 |
| `user_name` | string \| null | Имя пользователя | "Иван Петров" |
| `rating` | integer | Рейтинг от 1 до 5 | 5 |
| `comment` | string \| null | Текст отзыва | "Отличный сервис!" |
| `created_at` | datetime | Дата и время создания отзыва (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Пользовательские эндпоинты

### POST /api/v1/service-stations/
Создание новой СТО (требует модерации)

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "name": "Автосервис ПоЧо",
  "address": "Амира Темура, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@service.uz",
  "website": "https://service.uz",
  "is_24_7": false,
  "working_hours": "08:00-20:00",
  "description": "Полный спектр услуг по ремонту автомобилей",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "category": "СТО",
  "service_prices": [
    {
      "service_type": "Замена масла",
      "service_name": "Замена масла двигателя",
      "price": 150000,
      "description": "Замена моторного масла с фильтром"
    },
    {
      "service_type": "Ремонт двигателя",
      "service_name": "Диагностика двигателя",
      "price": 200000,
      "description": "Компьютерная диагностика двигателя"
    },
    {
      "service_type": "Шиномонтаж",
      "service_name": "Замена шин",
      "price": 50000,
      "description": "Снятие и установка шин"
    }
  ]
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "name": "Автосервис ПоЧо",
  "address": "Амира Темура, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@service.uz",
  "website": "https://service.uz",
  "is_24_7": false,
  "working_hours": "08:00-20:00",
  "description": "Полный спектр услуг по ремонту автомобилей",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "category": "СТО",
  "rating": 0.0,
  "reviews_count": 0,
  "status": "pending",
  "has_promotions": false,
  "service_prices": [
    {
      "id": 1,
      "service_station_id": 1,
      "service_type": "Замена масла",
      "service_name": "Замена масла двигателя",
      "price": 150000.0,
      "description": "Замена моторного масла с фильтром",
      "updated_at": null
    }
  ],
  "photos": [],
  "main_photo": null,
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": null
}
```

**Ошибки:**
- `400 Bad Request` - Неверные данные запроса
- `401 Unauthorized` - Требуется авторизация
- `422 Unprocessable Entity` - Ошибка валидации данных

### GET /api/v1/service-stations/
Получение списка СТО с фильтрацией

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)
- `service_type` - Тип услуги (см. Типы услуг)
- `min_rating` - Минимальный рейтинг (0-5)
- `min_price` - Минимальная цена услуги
- `max_price` - Максимальная цена услуги
- `is_24_7` - Работает 24/7 (true/false)
- `has_promotions` - Есть акции (true/false)
- `has_parking` - Есть парковка (true/false)
- `has_waiting_room` - Есть комната ожидания (true/false)
- `has_cafe` - Есть кафе (true/false)
- `accepts_cards` - Принимает карты (true/false)
- `search_query` - Поиск по названию, адресу или описанию
- `latitude` - Широта для поиска по близости
- `longitude` - Долгота для поиска по близости
- `radius_km` - Радиус поиска в километрах

**Пример:**
```
GET /api/v1/service-stations/?service_type=Замена масла&min_rating=4.0&has_parking=true&accepts_cards=true
```

**Ответ:**
```json
{
  "service_stations": [...],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

### GET /api/v1/service-stations/{station_id}
Получение детальной информации о СТО

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID СТО

**Ответ (200 OK):**
```json
{
  "id": 1,
  "name": "Автосервис ПоЧо",
  "address": "Амира Темура, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@service.uz",
  "website": "https://service.uz",
  "is_24_7": false,
  "working_hours": "08:00-20:00",
  "description": "Полный спектр услуг по ремонту автомобилей",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "category": "СТО",
  "rating": 4.8,
  "reviews_count": 127,
  "status": "approved",
  "has_promotions": true,
  "service_prices": [...],
  "photos": [...],
  "main_photo": "http://localhost:8000/uploads/service_stations/1_abc123.jpg",
  "reviews": [...],
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `404 Not Found` - СТО не найдена или не одобрена
- `401 Unauthorized` - Требуется авторизация

### POST /api/v1/service-stations/{station_id}/photos
Загрузка фотографии для СТО

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID СТО

**Параметры запроса (query):**
- `is_main` (boolean, опционально) - Главная фотография (по умолчанию false)
- `order` (integer, опционально) - Порядок отображения (по умолчанию 0, минимум 0)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения (разрешены: image/jpeg, image/jpg, image/png, image/webp, максимум 5MB)

**Ответ (201 Created):**
```json
{
  "id": 1,
  "service_station_id": 1,
  "photo_url": "http://localhost:8000/uploads/service_stations/1_abc123.jpg",
  "is_main": true,
  "order": 0,
  "created_at": "2026-01-06T09:26:11.879Z"
}
```

**Ошибки:**
- `400 Bad Request` - Недопустимый тип файла или превышен размер
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Нет прав для добавления фотографий (только создатель или админ)
- `404 Not Found` - СТО не найдена

### DELETE /api/v1/service-stations/{station_id}/photos/{photo_id}
Удаление фотографии

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ (204 No Content):** Пустое тело ответа

### POST /api/v1/service-stations/{station_id}/service-prices
Обновление цен на услуги

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID СТО

**Запрос:** `BulkServicePriceUpdate`
```json
{
  "service_prices": [
    {
      "service_type": "Замена масла",
      "service_name": "Замена масла двигателя",
      "price": 150000,
      "description": "Замена моторного масла с фильтром"
    },
    {
      "service_type": "Ремонт двигателя",
      "service_name": "Диагностика двигателя",
      "price": 200000,
      "description": "Компьютерная диагностика двигателя"
    }
  ]
}
```

**Ответ:** Список обновленных цен (`List[ServicePriceResponse]`)
```json
[
  {
    "id": 1,
    "service_station_id": 1,
    "service_type": "Замена масла",
    "service_name": "Замена масла двигателя",
    "price": 150000.0,
    "description": "Замена моторного масла с фильтром",
    "updated_at": "2026-01-06T09:26:11.879Z"
  }
]
```

### POST /api/v1/service-stations/{station_id}/reviews
Создание отзыва о СТО

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID СТО

**Запрос:** `ServiceStationReviewCreate`
```json
{
  "rating": 5,
  "comment": "Отличный сервис! Быстро и качественно."
}
```

**Ответ (201 Created):** `ServiceStationReviewResponse`
```json
{
  "id": 1,
  "service_station_id": 1,
  "user_id": 5,
  "user_name": "Иван Петров",
  "rating": 5,
  "comment": "Отличный сервис! Быстро и качественно.",
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": null
}
```

### PUT /api/v1/service-stations/{station_id}/reviews/{review_id}
Обновление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/service-stations/{station_id}/reviews/{review_id}
Удаление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

## Администраторские эндпоинты

### POST /api/v1/admin/service-stations/
Создание СТО (сразу одобрена)

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

### GET /api/v1/admin/service-stations/
Получение списка всех СТО (включая ожидающие модерации)

**Параметры:**
- Все параметры из пользовательского эндпоинта
- `status` - Фильтр по статусу (pending, approved, rejected, archived)

### GET /api/v1/admin/service-stations/{station_id}
Получение детальной информации о СТО

### PUT /api/v1/admin/service-stations/{station_id}
Обновление СТО

**Запрос:**
```json
{
  "name": "Новое название",
  "has_promotions": true,
  "status": "approved"
}
```

### DELETE /api/v1/admin/service-stations/{station_id}
Удаление СТО

### POST /api/v1/admin/service-stations/{station_id}/approve
Одобрение СТО

### POST /api/v1/admin/service-stations/{station_id}/reject
Отклонение СТО

### POST /api/v1/admin/service-stations/{station_id}/photos
Загрузка фотографии

### DELETE /api/v1/admin/service-stations/{station_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/admin/service-stations/{station_id}/photos/{photo_id}/set-main
Установка главной фотографии

### POST /api/v1/admin/service-stations/{station_id}/service-prices
Обновление цен на услуги

## Статусы СТО

| Статус | Описание | Видимость для пользователей |
|--------|----------|------------------------------|
| `pending` | Ожидает модерации (СТО, созданные пользователями) | ❌ Не видна |
| `approved` | Одобрена администратором | ✅ Видна |
| `rejected` | Отклонена администратором | ❌ Не видна |
| `archived` | Архивирована (скрыта, но не удалена) | ❌ Не видна |

**Примечание:** Пользователи видят только СТО со статусом `approved`. Администраторы могут видеть и управлять всеми СТО.

## Типы услуг

Доступные типы услуг:
- `Замена масла` - Замена моторного масла
- `Ремонт двигателя` - Ремонт двигателя
- `Ремонт КПП` - Ремонт коробки передач
- `Ремонт тормозов` - Ремонт тормозной системы
- `Ремонт подвески` - Ремонт подвески
- `Ремонт электрооборудования` - Ремонт электрооборудования
- `Шиномонтаж` - Шиномонтаж
- `Развал-схождение` - Развал-схождение
- `Кузовной ремонт` - Кузовной ремонт
- `Покраска` - Покраска автомобиля
- `Диагностика` - Диагностика автомобиля
- `Техобслуживание` - Техническое обслуживание
- `Мойка` - Мойка автомобиля
- `Другое` - Другие услуги

## Особенности

1. **Модерация**: СТО, созданные пользователями, автоматически получают статус `pending` и требуют одобрения админом. СТО, созданные админами, сразу получают статус `approved`.

2. **Рейтинг**: Автоматически пересчитывается при добавлении, изменении или удалении отзывов. Формула: среднее арифметическое всех рейтингов отзывов, округленное до 2 знаков после запятой.

3. **Главная фотография**: Можно установить одну главную фотографию для СТО. При установке новой главной фотографии предыдущая автоматически перестает быть главной.

4. **Цены на услуги**: Можно указать несколько типов услуг с ценами. Каждая услуга может иметь свое название и описание.

5. **Фильтрация**: Поддерживается фильтрация по типу услуги, рейтингу, цене, режиму работы, наличию акций, дополнительным услугам (парковка, комната ожидания, кафе, прием карт) и поиск по названию/адресу/описанию.

6. **Поиск по близости**: Можно искать СТО в радиусе от указанных координат используя формулу гаверсинуса. Радиус указывается в километрах.

7. **Отзывы**: Один пользователь может оставить только один отзыв на СТО. При повторной отправке отзыва существующий отзыв обновляется.

8. **Права доступа**: 
   - Пользователи могут создавать СТО, добавлять фотографии и обновлять цены только для своих СТО
   - Администраторы имеют полный доступ ко всем операциям

## Ограничения

- Максимальный размер файла фотографии: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка СТО в одном запросе: 1000 записей
- Рейтинг в отзывах: от 1 до 5 (целое число)
- Координаты: широта от -90 до 90, долгота от -180 до 180

## Примеры использования

### Создание СТО пользователем
```bash
curl -X POST "http://localhost:8000/api/v1/service-stations/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Автосервис ПоЧо",
    "address": "Амира Темура, 15, Tashkent",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "phone": "+998 90 123 45 67",
    "has_parking": true,
    "has_waiting_room": true,
    "accepts_cards": true,
    "service_prices": [
      {
        "service_type": "Замена масла",
        "service_name": "Замена масла двигателя",
        "price": 150000
      }
    ]
  }'
```

### Поиск СТО с фильтрацией
```bash
curl -X GET "http://localhost:8000/api/v1/service-stations/?service_type=Замена масла&min_rating=4.0&has_parking=true&accepts_cards=true" \
  -H "Authorization: Bearer <token>"
```

### Загрузка фотографии
```bash
curl -X POST "http://localhost:8000/api/v1/service-stations/1/photos?is_main=true" \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

### Обновление цен на услуги
```bash
curl -X POST "http://localhost:8000/api/v1/service-stations/1/service-prices" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "service_prices": [
      {
        "service_type": "Замена масла",
        "service_name": "Замена масла двигателя",
        "price": 150000,
        "description": "Замена моторного масла с фильтром"
      },
      {
        "service_type": "Ремонт двигателя",
        "service_name": "Диагностика двигателя",
        "price": 200000
      }
    ]
  }'
```

### Создание отзыва
```bash
curl -X POST "http://localhost:8000/api/v1/service-stations/1/reviews" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Отличный сервис!"
  }'
```

