# API для заправочных станций

## Описание

Система управления заправочными станциями с поддержкой:
- Добавления станций (пользователями и админами)
- Управления ценами на топливо
- Загрузки фотографий
- Отзывов и рейтингов
- Фильтрации по различным параметрам
- Поиска по близости

## Модели данных

### GasStation (Заправочная станция)

#### Поля для создания/обновления (GasStationCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название заправочной станции (1-255 символов) | "PoCho City Station" |
| `address` | string | ✅ Да | Полный адрес станции (минимум 1 символ) | "Mustaqillik ko'chasi, 10, Tashkent" |
| `latitude` | float | ✅ Да | Широта в градусах (-90 до 90) | 41.3111 |
| `longitude` | float | ✅ Да | Долгота в градусах (-180 до 180) | 69.2797 |
| `phone` | string | ❌ Нет | Номер телефона | "+998 90 123 45 67" |
| `is_24_7` | boolean | ❌ Нет | Работает ли станция круглосуточно (по умолчанию false) | true |
| `working_hours` | string | ❌ Нет | Режим работы (если не 24/7) | "08:00-22:00" |
| `category` | string | ❌ Нет | Категория станции (по умолчанию "Заправка") | "Заправка" |
| `fuel_prices` | array | ❌ Нет | Массив цен на топливо (см. FuelPriceCreate) | см. ниже |

#### Поля в ответе (GasStationResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор станции | 1 |
| `name` | string | Название заправочной станции | "PoCho City Station" |
| `address` | string | Полный адрес станции | "Mustaqillik ko'chasi, 10, Tashkent" |
| `latitude` | float | Широта в градусах | 41.3111 |
| `longitude` | float | Долгота в градусах | 69.2797 |
| `phone` | string \| null | Номер телефона | "+998 90 123 45 67" |
| `is_24_7` | boolean | Работает ли станция круглосуточно | true |
| `working_hours` | string \| null | Режим работы | "08:00-22:00" |
| `category` | string | Категория станции | "Заправка" |
| `rating` | float | Средний рейтинг (0.0-5.0), автоматически рассчитывается | 4.8 |
| `reviews_count` | integer | Количество отзывов, автоматически обновляется | 127 |
| `status` | string | Статус станции: `pending`, `approved`, `rejected`, `archived` | "approved" |
| `has_promotions` | boolean | Есть ли акции/промо-предложения | true |
| `fuel_prices` | array | Массив цен на топливо (см. FuelPriceResponse) | см. ниже |
| `photos` | array | Массив фотографий станции (см. GasStationPhotoResponse) | см. ниже |
| `main_photo` | string \| null | URL главной фотографии станции | "http://localhost:8000/uploads/gas_stations/1_abc123.jpg" |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### FuelPrice (Цена на топливо)

#### Поля для создания/обновления (FuelPriceCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `fuel_type` | string | ✅ Да | Тип топлива: `AI-80`, `AI-91`, `AI-95`, `AI-98`, `Дизель`, `Газ` | "AI-95" |
| `price` | float | ✅ Да | Цена в сумах (должна быть больше 0) | 12500.0 |

#### Поля в ответе (FuelPriceResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор цены | 1 |
| `gas_station_id` | integer | ID заправочной станции | 1 |
| `fuel_type` | string | Тип топлива | "AI-95" |
| `price` | float | Цена в сумах | 12500.0 |
| `updated_at` | datetime \| null | Дата и время последнего обновления цены (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### GasStationPhoto (Фотография)

#### Поля для создания (GasStationPhotoCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `is_main` | boolean | ❌ Нет | Является ли фотография главной (по умолчанию false) | true |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

**Примечание:** Файл загружается через `multipart/form-data` с полем `file`.

#### Поля в ответе (GasStationPhotoResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор фотографии | 1 |
| `gas_station_id` | integer | ID заправочной станции | 1 |
| `photo_url` | string | Полный URL фотографии | "http://localhost:8000/uploads/gas_stations/1_abc123.jpg" |
| `is_main` | boolean | Является ли фотография главной | true |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время загрузки (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### Review (Отзыв)

#### Поля для создания/обновления (ReviewCreate/ReviewUpdate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `rating` | integer | ✅ Да | Рейтинг от 1 до 5 | 5 |
| `comment` | string | ❌ Нет | Текст отзыва | "Отличная заправка! Всегда чисто, быстрое обслуживание." |

#### Поля в ответе (ReviewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор отзыва | 1 |
| `gas_station_id` | integer | ID заправочной станции | 1 |
| `user_id` | integer | ID пользователя, оставившего отзыв | 5 |
| `user_name` | string \| null | Имя пользователя | "Иван Петров" |
| `rating` | integer | Рейтинг от 1 до 5 | 5 |
| `comment` | string \| null | Текст отзыва | "Отличная заправка!" |
| `created_at` | datetime | Дата и время создания отзыва (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Пользовательские эндпоинты

### POST /api/v1/gas-stations/
Создание новой заправочной станции (требует модерации)

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "name": "PoCho City Station",
  "address": "Mustaqillik ko'chasi, 10, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "is_24_7": true,
  "working_hours": null,
  "category": "Заправка",
  "fuel_prices": [
    {
      "fuel_type": "AI-95",
      "price": 12500
    },
    {
      "fuel_type": "AI-91",
      "price": 11800
    },
    {
      "fuel_type": "Дизель",
      "price": 12000
    }
  ]
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "name": "PoCho City Station",
  "address": "Mustaqillik ko'chasi, 10, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "is_24_7": true,
  "working_hours": null,
  "category": "Заправка",
  "rating": 0.0,
  "reviews_count": 0,
  "status": "pending",
  "has_promotions": false,
  "fuel_prices": [
    {
      "id": 1,
      "gas_station_id": 1,
      "fuel_type": "AI-95",
      "price": 12500.0,
      "updated_at": "2026-01-06T09:26:11.879Z"
    },
    {
      "id": 2,
      "gas_station_id": 1,
      "fuel_type": "AI-91",
      "price": 11800.0,
      "updated_at": "2026-01-06T09:26:11.879Z"
    },
    {
      "id": 3,
      "gas_station_id": 1,
      "fuel_type": "Дизель",
      "price": 12000.0,
      "updated_at": "2026-01-06T09:26:11.879Z"
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

### GET /api/v1/gas-stations/
Получение списка заправочных станций с фильтрацией

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)
- `fuel_type` - Тип топлива (AI-80, AI-91, AI-95, AI-98, Дизель, Газ)
- `min_rating` - Минимальный рейтинг (0-5)
- `max_price` - Максимальная цена
- `is_24_7` - Работает 24/7 (true/false)
- `has_promotions` - Есть акции (true/false)
- `search_query` - Поиск по названию или адресу
- `latitude` - Широта для поиска по близости
- `longitude` - Долгота для поиска по близости
- `radius_km` - Радиус поиска в километрах

**Пример:**
```
GET /api/v1/gas-stations/?fuel_type=AI-95&min_rating=4.0&max_price=13000&is_24_7=true
```

**Ответ:**
```json
{
  "stations": [...],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

### GET /api/v1/gas-stations/{station_id}
Получение детальной информации о заправочной станции

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции

**Ответ (200 OK):**
```json
{
  "id": 1,
  "name": "PoCho City Station",
  "address": "Mustaqillik ko'chasi, 10, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "is_24_7": true,
  "working_hours": null,
  "category": "Заправка",
  "rating": 4.8,
  "reviews_count": 127,
  "status": "approved",
  "has_promotions": true,
  "fuel_prices": [
    {
      "id": 1,
      "gas_station_id": 1,
      "fuel_type": "AI-95",
      "price": 12500.0,
      "updated_at": "2026-01-06T09:26:11.879Z"
    },
    {
      "id": 2,
      "gas_station_id": 1,
      "fuel_type": "AI-91",
      "price": 11800.0,
      "updated_at": "2026-01-06T09:26:11.879Z"
    }
  ],
  "photos": [
    {
      "id": 1,
      "gas_station_id": 1,
      "photo_url": "http://localhost:8000/uploads/gas_stations/1_abc123.jpg",
      "is_main": true,
      "order": 0,
      "created_at": "2026-01-06T09:26:11.879Z"
    }
  ],
  "main_photo": "http://localhost:8000/uploads/gas_stations/1_abc123.jpg",
  "reviews": [
    {
      "id": 1,
      "gas_station_id": 1,
      "user_id": 5,
      "user_name": "Иван Петров",
      "rating": 5,
      "comment": "Отличная заправка! Всегда чисто, быстрое обслуживание.",
      "created_at": "2026-01-04T09:26:11.879Z",
      "updated_at": null
    },
    {
      "id": 2,
      "gas_station_id": 1,
      "user_id": 6,
      "user_name": "Мария Сидорова",
      "rating": 4,
      "comment": "Хорошее качество топлива. Единственный минус - иногда очереди.",
      "created_at": "2026-01-01T09:26:11.879Z",
      "updated_at": null
    }
  ],
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `404 Not Found` - Станция не найдена или не одобрена
- `401 Unauthorized` - Требуется авторизация

### POST /api/v1/gas-stations/{station_id}/photos
Загрузка фотографии для заправочной станции

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции

**Параметры запроса (query):**
- `is_main` (boolean, опционально) - Главная фотография (по умолчанию false)
- `order` (integer, опционально) - Порядок отображения (по умолчанию 0, минимум 0)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения (разрешены: image/jpeg, image/jpg, image/png, image/webp, максимум 5MB)

**Ответ (201 Created):**
```json
{
  "id": 1,
  "gas_station_id": 1,
  "photo_url": "http://localhost:8000/uploads/gas_stations/1_abc123.jpg",
  "is_main": true,
  "order": 0,
  "created_at": "2026-01-06T09:26:11.879Z"
}
```

**Ошибки:**
- `400 Bad Request` - Недопустимый тип файла или превышен размер
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Нет прав для добавления фотографий (только создатель или админ)
- `404 Not Found` - Станция не найдена

### DELETE /api/v1/gas-stations/{station_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/gas-stations/{station_id}/fuel-prices
Обновление цен на топливо

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции

**Запрос (Content-Type: application/json):**
```json
{
  "fuel_prices": [
    {
      "fuel_type": "AI-95",
      "price": 12500
    },
    {
      "fuel_type": "AI-91",
      "price": 11800
    },
    {
      "fuel_type": "Дизель",
      "price": 12000
    }
  ]
}
```

**Ответ (200 OK):**
```json
[
  {
    "fuel_type": "AI-95",
    "price": 12500
  },
  {
    "fuel_type": "AI-91",
    "price": 11800
  },
  {
    "fuel_type": "Дизель",
    "price": 12000
  }
]
```

**Ошибки:**
- `400 Bad Request` - Неверные данные запроса
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Нет прав для обновления цен (только создатель или админ)
- `404 Not Found` - Станция не найдена
- `422 Unprocessable Entity` - Ошибка валидации данных

### POST /api/v1/gas-stations/{station_id}/reviews
Создание отзыва о заправочной станции

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции

**Запрос (Content-Type: application/json):**
```json
{
  "rating": 5,
  "comment": "Отличная заправка! Всегда чисто, быстрое обслуживание."
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "gas_station_id": 1,
  "user_id": 5,
  "user_name": "Иван Петров",
  "rating": 5,
  "comment": "Отличная заправка! Всегда чисто, быстрое обслуживание.",
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": null
}
```

**Примечание:** Если отзыв от данного пользователя уже существует, он будет обновлен.

**Ошибки:**
- `400 Bad Request` - Неверные данные запроса
- `401 Unauthorized` - Требуется авторизация
- `404 Not Found` - Станция не найдена или не одобрена
- `422 Unprocessable Entity` - Ошибка валидации данных (например, рейтинг вне диапазона 1-5)

### PUT /api/v1/gas-stations/{station_id}/reviews/{review_id}
Обновление отзыва о заправочной станции

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции
- `review_id` (integer, обязательный) - ID отзыва

**Запрос (Content-Type: application/json):**
```json
{
  "rating": 4,
  "comment": "Хорошая заправка, но иногда очереди."
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "gas_station_id": 1,
  "user_id": 5,
  "user_name": "Иван Петров",
  "rating": 4,
  "comment": "Хорошая заправка, но иногда очереди.",
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `401 Unauthorized` - Требуется авторизация
- `404 Not Found` - Отзыв не найден или принадлежит другому пользователю
- `422 Unprocessable Entity` - Ошибка валидации данных

### DELETE /api/v1/gas-stations/{station_id}/reviews/{review_id}
Удаление отзыва о заправочной станции

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции
- `review_id` (integer, обязательный) - ID отзыва

**Ответ (204 No Content):** Пустое тело ответа

**Ошибки:**
- `401 Unauthorized` - Требуется авторизация
- `404 Not Found` - Отзыв не найден или принадлежит другому пользователю

## Администраторские эндпоинты

### POST /api/v1/admin/gas-stations/
Создание заправочной станции (сразу одобрена)

### GET /api/v1/admin/gas-stations/
Получение списка всех станций (включая ожидающие модерации)

**Параметры:**
- Все параметры из пользовательского эндпоинта
- `status` - Фильтр по статусу (pending, approved, rejected, archived)

### GET /api/v1/admin/gas-stations/{station_id}
Получение детальной информации о станции

### PUT /api/v1/admin/gas-stations/{station_id}
Обновление заправочной станции

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

**Параметры пути:**
- `station_id` (integer, обязательный) - ID заправочной станции

**Запрос (Content-Type: application/json):**
Все поля опциональны, обновляются только переданные:
```json
{
  "name": "Новое название",
  "address": "Новый адрес",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "is_24_7": true,
  "working_hours": "08:00-22:00",
  "category": "Заправка",
  "has_promotions": true,
  "status": "approved"
}
```

**Ответ (200 OK):**
```json
{
  "id": 1,
  "name": "Новое название",
  "address": "Новый адрес",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "is_24_7": true,
  "working_hours": "08:00-22:00",
  "category": "Заправка",
  "rating": 4.8,
  "reviews_count": 127,
  "status": "approved",
  "has_promotions": true,
  "fuel_prices": [...],
  "photos": [...],
  "main_photo": "...",
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Требуются права администратора
- `404 Not Found` - Станция не найдена
- `422 Unprocessable Entity` - Ошибка валидации данных

### DELETE /api/v1/admin/gas-stations/{station_id}
Удаление станции

### POST /api/v1/admin/gas-stations/{station_id}/approve
Одобрение станции

### POST /api/v1/admin/gas-stations/{station_id}/reject
Отклонение станции

### POST /api/v1/admin/gas-stations/{station_id}/photos
Загрузка фотографии

### DELETE /api/v1/admin/gas-stations/{station_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/admin/gas-stations/{station_id}/photos/{photo_id}/set-main
Установка главной фотографии

### POST /api/v1/admin/gas-stations/{station_id}/fuel-prices
Обновление цен на топливо

## Примеры использования

### Создание станции пользователем
```bash
curl -X POST "http://localhost:8000/api/v1/gas-stations/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PoCho City Station",
    "address": "Mustaqillik ko'\''chasi, 10, Tashkent",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "phone": "+998 90 123 45 67",
    "is_24_7": true,
    "fuel_prices": [
      {"fuel_type": "AI-95", "price": 12500},
      {"fuel_type": "AI-91", "price": 11800}
    ]
  }'
```

### Поиск станций с фильтрацией
```bash
curl -X GET "http://localhost:8000/api/v1/gas-stations/?fuel_type=AI-95&min_rating=4.0&max_price=13000&is_24_7=true" \
  -H "Authorization: Bearer <token>"
```

### Загрузка фотографии
```bash
curl -X POST "http://localhost:8000/api/v1/gas-stations/1/photos?is_main=true" \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

### Обновление цен на топливо
```bash
curl -X POST "http://localhost:8000/api/v1/gas-stations/1/fuel-prices" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "fuel_prices": [
      {"fuel_type": "AI-95", "price": 12500},
      {"fuel_type": "AI-91", "price": 11800},
      {"fuel_type": "Дизель", "price": 12000}
    ]
  }'
```

### Создание отзыва
```bash
curl -X POST "http://localhost:8000/api/v1/gas-stations/1/reviews" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Отличная заправка!"
  }'
```

## Статусы заправочных станций

| Статус | Описание | Видимость для пользователей |
|--------|----------|------------------------------|
| `pending` | Ожидает модерации (станции, созданные пользователями) | ❌ Не видна |
| `approved` | Одобрена администратором | ✅ Видна |
| `rejected` | Отклонена администратором | ❌ Не видна |
| `archived` | Архивирована (скрыта, но не удалена) | ❌ Не видна |

**Примечание:** Пользователи видят только станции со статусом `approved`. Администраторы могут видеть и управлять всеми станциями.

## Типы топлива

Доступные типы топлива:
- `AI-80` - Бензин АИ-80
- `AI-91` - Бензин АИ-91
- `AI-95` - Бензин АИ-95
- `AI-98` - Бензин АИ-98
- `Дизель` - Дизельное топливо
- `Газ` - Сжиженный газ

## Особенности

1. **Модерация**: Станции, созданные пользователями, автоматически получают статус `pending` и требуют одобрения админом. Станции, созданные админами, сразу получают статус `approved`.

2. **Рейтинг**: Автоматически пересчитывается при добавлении, изменении или удалении отзывов. Формула: среднее арифметическое всех рейтингов отзывов, округленное до 2 знаков после запятой.

3. **Главная фотография**: Можно установить одну главную фотографию для станции. При установке новой главной фотографии предыдущая автоматически перестает быть главной.

4. **Фильтрация**: Поддерживается фильтрация по типу топлива, рейтингу, цене, режиму работы, наличию акций и поиск по названию/адресу.

5. **Поиск по близости**: Можно искать станции в радиусе от указанных координат используя формулу гаверсинуса. Радиус указывается в километрах.

6. **Цены на топливо**: Можно указать несколько типов топлива с ценами. При обновлении цен, если цена для данного типа топлива уже существует, она обновляется, иначе создается новая запись.

7. **Отзывы**: Один пользователь может оставить только один отзыв на станцию. При повторной отправке отзыва существующий отзыв обновляется.

8. **Права доступа**: 
   - Пользователи могут создавать станции, добавлять фотографии и обновлять цены только для своих станций
   - Администраторы имеют полный доступ ко всем операциям

## Ограничения

- Максимальный размер файла фотографии: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка станций в одном запросе: 1000 записей
- Рейтинг в отзывах: от 1 до 5 (целое число)
- Координаты: широта от -90 до 90, долгота от -180 до 180

