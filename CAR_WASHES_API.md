# API для автомоек

## Описание

Система управления автомойками с поддержкой:
- Добавления автомоек (пользователями и админами)
- Управления ценами на услуги
- Загрузки фотографий
- Отзывов и рейтингов
- Фильтрации по различным параметрам
- Поиска по близости

## Модели данных

### CarWash (Автомойка)

#### Поля для создания/обновления (CarWashCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название автомойки (1-255 символов) | "Автомойка ПоЧо" |
| `address` | string | ✅ Да | Полный адрес автомойки (минимум 1 символ) | "Амира Темура, 20, Tashkent" |
| `latitude` | float | ✅ Да | Широта в градусах (-90 до 90) | 41.3111 |
| `longitude` | float | ✅ Да | Долгота в градусах (-180 до 180) | 69.2797 |
| `phone` | string | ❌ Нет | Номер телефона | "+998 90 123 45 67" |
| `email` | string | ❌ Нет | Email адрес | "info@carwash.uz" |
| `website` | string | ❌ Нет | Сайт автомойки | "https://carwash.uz" |
| `is_24_7` | boolean | ❌ Нет | Работает ли автомойка круглосуточно (по умолчанию false) | false |
| `working_hours` | string | ❌ Нет | Режим работы (если не 24/7) | "08:00-22:00" |
| `description` | string | ❌ Нет | Описание автомойки | "Современная автомойка с полным спектром услуг" |
| `has_parking` | boolean | ❌ Нет | Есть ли парковка (по умолчанию false) | true |
| `has_waiting_room` | boolean | ❌ Нет | Есть ли комната ожидания (по умолчанию false) | true |
| `has_cafe` | boolean | ❌ Нет | Есть ли кафе (по умолчанию false) | false |
| `accepts_cards` | boolean | ❌ Нет | Принимает ли карты (по умолчанию false) | true |
| `has_vacuum` | boolean | ❌ Нет | Есть ли пылесос (по умолчанию false) | true |
| `has_drying` | boolean | ❌ Нет | Есть ли сушка (по умолчанию false) | true |
| `has_self_service` | boolean | ❌ Нет | Есть ли самообслуживание (по умолчанию false) | false |
| `category` | string | ❌ Нет | Категория автомойки (по умолчанию "Автомойка") | "Автомойка" |
| `services` | array | ❌ Нет | Массив услуг (см. CarWashServiceCreate) | см. ниже |

#### Поля в ответе (CarWashResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор автомойки | 1 |
| `name` | string | Название автомойки | "Автомойка ПоЧо" |
| `address` | string | Полный адрес автомойки | "Амира Темура, 20, Tashkent" |
| `latitude` | float | Широта в градусах | 41.3111 |
| `longitude` | float | Долгота в градусах | 69.2797 |
| `phone` | string \| null | Номер телефона | "+998 90 123 45 67" |
| `email` | string \| null | Email адрес | "info@carwash.uz" |
| `website` | string \| null | Сайт автомойки | "https://carwash.uz" |
| `is_24_7` | boolean | Работает ли автомойка круглосуточно | false |
| `working_hours` | string \| null | Режим работы | "08:00-22:00" |
| `description` | string \| null | Описание автомойки | "Современная автомойка..." |
| `has_parking` | boolean | Есть ли парковка | true |
| `has_waiting_room` | boolean | Есть ли комната ожидания | true |
| `has_cafe` | boolean | Есть ли кафе | false |
| `accepts_cards` | boolean | Принимает ли карты | true |
| `has_vacuum` | boolean | Есть ли пылесос | true |
| `has_drying` | boolean | Есть ли сушка | true |
| `has_self_service` | boolean | Есть ли самообслуживание | false |
| `category` | string | Категория автомойки | "Автомойка" |
| `rating` | float | Средний рейтинг (0.0-5.0), автоматически рассчитывается | 4.8 |
| `reviews_count` | integer | Количество отзывов, автоматически обновляется | 127 |
| `status` | string | Статус автомойки: `pending`, `approved`, `rejected`, `archived` | "approved" |
| `has_promotions` | boolean | Есть ли акции/промо-предложения | true |
| `services` | array | Массив услуг (см. CarWashServiceResponse) | см. ниже |
| `photos` | array | Массив фотографий автомойки (см. CarWashPhotoResponse) | см. ниже |
| `main_photo` | string \| null | URL главной фотографии автомойки | "http://localhost:8000/uploads/car_washes/1_abc123.jpg" |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### CarWashService (Услуга автомойки)

#### Поля для создания/обновления (CarWashServiceCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `service_type` | string | ✅ Да | Тип услуги (см. Типы услуг) | "Ручная мойка" |
| `service_name` | string | ❌ Нет | Название конкретной услуги (до 255 символов) | "Ручная мойка кузова" |
| `price` | float | ✅ Да | Цена в сумах (должна быть больше 0) | 50000.0 |
| `description` | string | ❌ Нет | Описание услуги | "Ручная мойка кузова с шампунем" |
| `duration_minutes` | integer | ❌ Нет | Длительность услуги в минутах (минимум 1) | 30 |

#### Поля в ответе (CarWashServiceResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор услуги | 1 |
| `car_wash_id` | integer | ID автомойки | 1 |
| `service_type` | string | Тип услуги | "Ручная мойка" |
| `service_name` | string \| null | Название конкретной услуги | "Ручная мойка кузова" |
| `price` | float | Цена в сумах | 50000.0 |
| `description` | string \| null | Описание услуги | "Ручная мойка кузова с шампунем" |
| `duration_minutes` | integer \| null | Длительность услуги в минутах | 30 |
| `updated_at` | datetime \| null | Дата и время последнего обновления услуги (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### CarWashPhoto (Фотография)

#### Поля для создания (CarWashPhotoCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `is_main` | boolean | ❌ Нет | Является ли фотография главной (по умолчанию false) | true |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

**Примечание:** Файл загружается через `multipart/form-data` с полем `file`.

#### Поля в ответе (CarWashPhotoResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор фотографии | 1 |
| `car_wash_id` | integer | ID автомойки | 1 |
| `photo_url` | string | Полный URL фотографии | "http://localhost:8000/uploads/car_washes/1_abc123.jpg" |
| `is_main` | boolean | Является ли фотография главной | true |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время загрузки (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### CarWashReview (Отзыв)

#### Поля для создания/обновления (CarWashReviewCreate/CarWashReviewUpdate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `rating` | integer | ✅ Да | Рейтинг от 1 до 5 | 5 |
| `comment` | string | ❌ Нет | Текст отзыва | "Отличная автомойка! Чисто и быстро." |

#### Поля в ответе (CarWashReviewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор отзыва | 1 |
| `car_wash_id` | integer | ID автомойки | 1 |
| `user_id` | integer | ID пользователя, оставившего отзыв | 5 |
| `user_name` | string \| null | Имя пользователя | "Иван Петров" |
| `rating` | integer | Рейтинг от 1 до 5 | 5 |
| `comment` | string \| null | Текст отзыва | "Отличная автомойка!" |
| `created_at` | datetime | Дата и время создания отзыва (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Пользовательские эндпоинты

### POST /api/v1/car-washes/
Создание новой автомойки (требует модерации)

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "name": "Автомойка ПоЧо",
  "address": "Амира Темура, 20, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@carwash.uz",
  "website": "https://carwash.uz",
  "is_24_7": false,
  "working_hours": "08:00-22:00",
  "description": "Современная автомойка с полным спектром услуг",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "has_vacuum": true,
  "has_drying": true,
  "has_self_service": false,
  "category": "Автомойка",
  "services": [
    {
      "service_type": "Ручная мойка",
      "service_name": "Ручная мойка кузова",
      "price": 50000,
      "description": "Ручная мойка кузова с шампунем",
      "duration_minutes": 30
    },
    {
      "service_type": "Химчистка",
      "service_name": "Химчистка салона",
      "price": 200000,
      "description": "Полная химчистка салона автомобиля",
      "duration_minutes": 120
    },
    {
      "service_type": "Полировка",
      "service_name": "Полировка кузова",
      "price": 300000,
      "description": "Полировка кузова с защитным покрытием",
      "duration_minutes": 180
    }
  ]
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "name": "Автомойка ПоЧо",
  "address": "Амира Темура, 20, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@carwash.uz",
  "website": "https://carwash.uz",
  "is_24_7": false,
  "working_hours": "08:00-22:00",
  "description": "Современная автомойка с полным спектром услуг",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "has_vacuum": true,
  "has_drying": true,
  "has_self_service": false,
  "category": "Автомойка",
  "rating": 0.0,
  "reviews_count": 0,
  "status": "pending",
  "has_promotions": false,
  "services": [
    {
      "id": 1,
      "car_wash_id": 1,
      "service_type": "Ручная мойка",
      "service_name": "Ручная мойка кузова",
      "price": 50000.0,
      "description": "Ручная мойка кузова с шампунем",
      "duration_minutes": 30,
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

### GET /api/v1/car-washes/
Получение списка автомоек с фильтрацией

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
- `has_vacuum` - Есть пылесос (true/false)
- `has_drying` - Есть сушка (true/false)
- `has_self_service` - Есть самообслуживание (true/false)
- `search_query` - Поиск по названию, адресу или описанию
- `latitude` - Широта для поиска по близости
- `longitude` - Долгота для поиска по близости
- `radius_km` - Радиус поиска в километрах

**Пример:**
```
GET /api/v1/car-washes/?service_type=Ручная мойка&min_rating=4.0&has_parking=true&has_vacuum=true
```

**Ответ:**
```json
{
  "car_washes": [...],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

### GET /api/v1/car-washes/{car_wash_id}
Получение детальной информации об автомойке

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `car_wash_id` (integer, обязательный) - ID автомойки

**Ответ (200 OK):**
```json
{
  "id": 1,
  "name": "Автомойка ПоЧо",
  "address": "Амира Темура, 20, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@carwash.uz",
  "website": "https://carwash.uz",
  "is_24_7": false,
  "working_hours": "08:00-22:00",
  "description": "Современная автомойка с полным спектром услуг",
  "has_parking": true,
  "has_waiting_room": true,
  "has_cafe": false,
  "accepts_cards": true,
  "has_vacuum": true,
  "has_drying": true,
  "has_self_service": false,
  "category": "Автомойка",
  "rating": 4.8,
  "reviews_count": 127,
  "status": "approved",
  "has_promotions": true,
  "services": [...],
  "photos": [...],
  "main_photo": "http://localhost:8000/uploads/car_washes/1_abc123.jpg",
  "reviews": [...],
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `404 Not Found` - Автомойка не найдена или не одобрена
- `401 Unauthorized` - Требуется авторизация

### POST /api/v1/car-washes/{car_wash_id}/photos
Загрузка фотографии для автомойки

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `car_wash_id` (integer, обязательный) - ID автомойки

**Параметры запроса (query):**
- `is_main` (boolean, опционально) - Главная фотография (по умолчанию false)
- `order` (integer, опционально) - Порядок отображения (по умолчанию 0, минимум 0)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения (разрешены: image/jpeg, image/jpg, image/png, image/webp, максимум 5MB)

**Ответ (201 Created):**
```json
{
  "id": 1,
  "car_wash_id": 1,
  "photo_url": "http://localhost:8000/uploads/car_washes/1_abc123.jpg",
  "is_main": true,
  "order": 0,
  "created_at": "2026-01-06T09:26:11.879Z"
}
```

**Ошибки:**
- `400 Bad Request` - Недопустимый тип файла или превышен размер
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Нет прав для добавления фотографий (только создатель или админ)
- `404 Not Found` - Автомойка не найдена

### DELETE /api/v1/car-washes/{car_wash_id}/photos/{photo_id}
Удаление фотографии

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ (204 No Content):** Пустое тело ответа

### POST /api/v1/car-washes/{car_wash_id}/services
Обновление услуг автомойки

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `car_wash_id` (integer, обязательный) - ID автомойки

**Запрос:** `BulkCarWashServiceUpdate`
```json
{
  "services": [
    {
      "service_type": "Ручная мойка",
      "service_name": "Ручная мойка кузова",
      "price": 50000,
      "description": "Ручная мойка кузова с шампунем",
      "duration_minutes": 30
    },
    {
      "service_type": "Химчистка",
      "service_name": "Химчистка салона",
      "price": 200000,
      "description": "Полная химчистка салона",
      "duration_minutes": 120
    }
  ]
}
```

**Ответ:** Список обновленных услуг (`List[CarWashServiceResponse]`)

### POST /api/v1/car-washes/{car_wash_id}/reviews
Создание отзыва об автомойке

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `car_wash_id` (integer, обязательный) - ID автомойки

**Запрос:** `CarWashReviewCreate`
```json
{
  "rating": 5,
  "comment": "Отличная автомойка! Чисто и быстро."
}
```

**Ответ (201 Created):** `CarWashReviewResponse`

### PUT /api/v1/car-washes/{car_wash_id}/reviews/{review_id}
Обновление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/car-washes/{car_wash_id}/reviews/{review_id}
Удаление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

## Администраторские эндпоинты

### POST /api/v1/admin/car-washes/
Создание автомойки (сразу одобрена)

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

### GET /api/v1/admin/car-washes/
Получение списка всех автомоек (включая ожидающие модерации)

**Параметры:**
- Все параметры из пользовательского эндпоинта
- `status` - Фильтр по статусу (pending, approved, rejected, archived)

### GET /api/v1/admin/car-washes/{car_wash_id}
Получение детальной информации об автомойке

### PUT /api/v1/admin/car-washes/{car_wash_id}
Обновление автомойки

**Запрос:**
```json
{
  "name": "Новое название",
  "has_promotions": true,
  "status": "approved"
}
```

### DELETE /api/v1/admin/car-washes/{car_wash_id}
Удаление автомойки

### POST /api/v1/admin/car-washes/{car_wash_id}/approve
Одобрение автомойки

### POST /api/v1/admin/car-washes/{car_wash_id}/reject
Отклонение автомойки

### POST /api/v1/admin/car-washes/{car_wash_id}/photos
Загрузка фотографии

### DELETE /api/v1/admin/car-washes/{car_wash_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/admin/car-washes/{car_wash_id}/photos/{photo_id}/set-main
Установка главной фотографии

### POST /api/v1/admin/car-washes/{car_wash_id}/services
Обновление услуг

## Статусы автомоек

| Статус | Описание | Видимость для пользователей |
|--------|----------|------------------------------|
| `pending` | Ожидает модерации (автомойки, созданные пользователями) | ❌ Не видна |
| `approved` | Одобрена администратором | ✅ Видна |
| `rejected` | Отклонена администратором | ❌ Не видна |
| `archived` | Архивирована (скрыта, но не удалена) | ❌ Не видна |

**Примечание:** Пользователи видят только автомойки со статусом `approved`. Администраторы могут видеть и управлять всеми автомойками.

## Типы услуг

Доступные типы услуг:
- `Ручная мойка` - Ручная мойка автомобиля
- `Автоматическая мойка` - Автоматическая мойка
- `Химчистка` - Химчистка салона
- `Полировка` - Полировка кузова
- `Нанесение воска` - Нанесение защитного воска
- `Пылесос` - Пылесос салона
- `Мойка двигателя` - Мойка двигателя
- `Мойка днища` - Мойка днища автомобиля
- `Чистка салона` - Чистка салона
- `Обработка кожи` - Обработка кожаных элементов салона
- `Чистка шин` - Чистка и обработка шин
- `Другое` - Другие услуги

## Особенности

1. **Модерация**: Автомойки, созданные пользователями, автоматически получают статус `pending` и требуют одобрения админом. Автомойки, созданные админами, сразу получают статус `approved`.

2. **Рейтинг**: Автоматически пересчитывается при добавлении, изменении или удалении отзывов. Формула: среднее арифметическое всех рейтингов отзывов, округленное до 2 знаков после запятой.

3. **Главная фотография**: Можно установить одну главную фотографию для автомойки. При установке новой главной фотографии предыдущая автоматически перестает быть главной.

4. **Услуги**: Можно указать несколько типов услуг с ценами. Каждая услуга может иметь свое название, описание и длительность.

5. **Фильтрация**: Поддерживается фильтрация по типу услуги, рейтингу, цене, режиму работы, наличию акций, дополнительным услугам (парковка, комната ожидания, кафе, прием карт, пылесос, сушка, самообслуживание) и поиск по названию/адресу/описанию.

6. **Поиск по близости**: Можно искать автомойки в радиусе от указанных координат используя формулу гаверсинуса. Радиус указывается в километрах.

7. **Отзывы**: Один пользователь может оставить только один отзыв на автомойку. При повторной отправке отзыва существующий отзыв обновляется.

8. **Права доступа**: 
   - Пользователи могут создавать автомойки, добавлять фотографии и обновлять услуги только для своих автомоек
   - Администраторы имеют полный доступ ко всем операциям

## Ограничения

- Максимальный размер файла фотографии: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка автомоек в одном запросе: 1000 записей
- Рейтинг в отзывах: от 1 до 5 (целое число)
- Координаты: широта от -90 до 90, долгота от -180 до 180

## Примеры использования

### Создание автомойки пользователем
```bash
curl -X POST "http://localhost:8000/api/v1/car-washes/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Автомойка ПоЧо",
    "address": "Амира Темура, 20, Tashkent",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "phone": "+998 90 123 45 67",
    "has_parking": true,
    "has_vacuum": true,
    "has_drying": true,
    "accepts_cards": true,
    "services": [
      {
        "service_type": "Ручная мойка",
        "service_name": "Ручная мойка кузова",
        "price": 50000,
        "duration_minutes": 30
      }
    ]
  }'
```

### Поиск автомоек с фильтрацией
```bash
curl -X GET "http://localhost:8000/api/v1/car-washes/?service_type=Ручная мойка&min_rating=4.0&has_parking=true&has_vacuum=true" \
  -H "Authorization: Bearer <token>"
```

### Загрузка фотографии
```bash
curl -X POST "http://localhost:8000/api/v1/car-washes/1/photos?is_main=true" \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

### Обновление услуг
```bash
curl -X POST "http://localhost:8000/api/v1/car-washes/1/services" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "services": [
      {
        "service_type": "Ручная мойка",
        "service_name": "Ручная мойка кузова",
        "price": 50000,
        "description": "Ручная мойка кузова с шампунем",
        "duration_minutes": 30
      },
      {
        "service_type": "Химчистка",
        "service_name": "Химчистка салона",
        "price": 200000,
        "duration_minutes": 120
      }
    ]
  }'
```

### Создание отзыва
```bash
curl -X POST "http://localhost:8000/api/v1/car-washes/1/reviews" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Отличная автомойка!"
  }'
```




