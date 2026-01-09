# API для ресторанов

## Описание

Система управления ресторанами с поддержкой:
- Добавления ресторанов (пользователями и админами)
- Управления меню (категории и блюда)
- Загрузки фотографий
- Отзывов и рейтингов
- Фильтрации по различным параметрам
- Поиска по близости

## Модели данных

### Restaurant (Ресторан)

#### Поля для создания/обновления (RestaurantCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название ресторана (1-255 символов) | "Ресторан Плов" |
| `address` | string | ✅ Да | Полный адрес ресторана (минимум 1 символ) | "Навои, 15, Tashkent" |
| `latitude` | float | ✅ Да | Широта в градусах (-90 до 90) | 41.3111 |
| `longitude` | float | ✅ Да | Долгота в градусах (-180 до 180) | 69.2797 |
| `phone` | string | ❌ Нет | Номер телефона | "+998 90 123 45 67" |
| `email` | string | ❌ Нет | Email адрес | "info@restaurant.uz" |
| `website` | string | ❌ Нет | Сайт ресторана | "https://restaurant.uz" |
| `is_24_7` | boolean | ❌ Нет | Работает ли ресторан круглосуточно (по умолчанию false) | false |
| `working_hours` | string | ❌ Нет | Режим работы (если не 24/7) | "09:00-23:00" |
| `cuisine_type` | string | ✅ Да | Тип кухни (см. Типы кухни) | "Узбекская" |
| `average_check` | float | ❌ Нет | Средний чек в сумах | 50000 |
| `has_booking` | boolean | ❌ Нет | Есть ли возможность бронирования (по умолчанию false) | true |
| `has_delivery` | boolean | ❌ Нет | Есть ли доставка (по умолчанию false) | true |
| `has_parking` | boolean | ❌ Нет | Есть ли парковка (по умолчанию false) | true |
| `has_wifi` | boolean | ❌ Нет | Есть ли Wi-Fi (по умолчанию false) | true |
| `category` | string | ❌ Нет | Категория ресторана (по умолчанию "Ресторан") | "Ресторан" |
| `description` | string | ❌ Нет | Описание ресторана | "Уютный ресторан с традиционной узбекской кухней" |
| `menu_categories` | array | ❌ Нет | Массив категорий меню с блюдами (см. MenuCategoryCreate) | см. ниже |

#### Поля в ответе (RestaurantResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор ресторана | 1 |
| `name` | string | Название ресторана | "Ресторан Плов" |
| `address` | string | Полный адрес ресторана | "Навои, 15, Tashkent" |
| `latitude` | float | Широта в градусах | 41.3111 |
| `longitude` | float | Долгота в градусах | 69.2797 |
| `phone` | string \| null | Номер телефона | "+998 90 123 45 67" |
| `email` | string \| null | Email адрес | "info@restaurant.uz" |
| `website` | string \| null | Сайт ресторана | "https://restaurant.uz" |
| `is_24_7` | boolean | Работает ли ресторан круглосуточно | false |
| `working_hours` | string \| null | Режим работы | "09:00-23:00" |
| `cuisine_type` | string | Тип кухни | "Узбекская" |
| `average_check` | float \| null | Средний чек в сумах | 50000.0 |
| `has_booking` | boolean | Есть ли возможность бронирования | true |
| `has_delivery` | boolean | Есть ли доставка | true |
| `has_parking` | boolean | Есть ли парковка | true |
| `has_wifi` | boolean | Есть ли Wi-Fi | true |
| `category` | string | Категория ресторана | "Ресторан" |
| `description` | string \| null | Описание ресторана | "Уютный ресторан..." |
| `rating` | float | Средний рейтинг (0.0-5.0), автоматически рассчитывается | 4.8 |
| `reviews_count` | integer | Количество отзывов, автоматически обновляется | 127 |
| `status` | string | Статус ресторана: `pending`, `approved`, `rejected`, `archived` | "approved" |
| `has_promotions` | boolean | Есть ли акции/промо-предложения | true |
| `menu_categories` | array | Массив категорий меню (см. MenuCategoryResponse) | см. ниже |
| `photos` | array | Массив фотографий ресторана (см. RestaurantPhotoResponse) | см. ниже |
| `main_photo` | string \| null | URL главной фотографии ресторана | "http://localhost:8000/uploads/restaurants/1_abc123.jpg" |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### MenuCategory (Категория меню)

#### Поля для создания (MenuCategoryCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название категории (1-255 символов) | "Супы" |
| `description` | string | ❌ Нет | Описание категории | "Горячие супы" |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |
| `items` | array | ❌ Нет | Массив блюд в категории (см. MenuItemCreate) | см. ниже |

#### Поля в ответе (MenuCategoryResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор категории | 1 |
| `restaurant_id` | integer | ID ресторана | 1 |
| `name` | string | Название категории | "Супы" |
| `description` | string \| null | Описание категории | "Горячие супы" |
| `order` | integer | Порядок отображения | 0 |
| `items` | array | Массив блюд в категории (см. MenuItemResponse) | см. ниже |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### MenuItem (Блюдо)

#### Поля для создания (MenuItemCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название блюда (1-255 символов) | "Плов" |
| `description` | string | ❌ Нет | Описание блюда | "Традиционный узбекский плов с мясом" |
| `price` | float | ✅ Да | Цена в сумах (должна быть больше 0) | 45000.0 |
| `image_url` | string | ❌ Нет | URL фотографии блюда | "http://localhost:8000/uploads/restaurants/menu_items/1_abc123.jpg" |
| `is_available` | boolean | ❌ Нет | Доступно ли блюдо (по умолчанию true) | true |
| `weight` | string | ❌ Нет | Вес/порция | "300г" |
| `calories` | integer | ❌ Нет | Калории (минимум 0) | 450 |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

#### Поля в ответе (MenuItemResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор блюда | 1 |
| `category_id` | integer | ID категории меню | 1 |
| `restaurant_id` | integer | ID ресторана | 1 |
| `name` | string | Название блюда | "Плов" |
| `description` | string \| null | Описание блюда | "Традиционный узбекский плов" |
| `price` | float | Цена в сумах | 45000.0 |
| `image_url` | string \| null | URL фотографии блюда | "http://localhost:8000/uploads/restaurants/menu_items/1_abc123.jpg" |
| `is_available` | boolean | Доступно ли блюдо | true |
| `weight` | string \| null | Вес/порция | "300г" |
| `calories` | integer \| null | Калории | 450 |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### RestaurantPhoto (Фотография)

#### Поля для создания (RestaurantPhotoCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `is_main` | boolean | ❌ Нет | Является ли фотография главной (по умолчанию false) | true |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

**Примечание:** Файл загружается через `multipart/form-data` с полем `file`.

#### Поля в ответе (RestaurantPhotoResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор фотографии | 1 |
| `restaurant_id` | integer | ID ресторана | 1 |
| `photo_url` | string | Полный URL фотографии | "http://localhost:8000/uploads/restaurants/1_abc123.jpg" |
| `is_main` | boolean | Является ли фотография главной | true |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время загрузки (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### RestaurantReview (Отзыв)

#### Поля для создания/обновления (RestaurantReviewCreate/RestaurantReviewUpdate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `rating` | integer | ✅ Да | Рейтинг от 1 до 5 | 5 |
| `comment` | string | ❌ Нет | Текст отзыва | "Отличный ресторан! Вкусная еда, быстрое обслуживание." |

#### Поля в ответе (RestaurantReviewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор отзыва | 1 |
| `restaurant_id` | integer | ID ресторана | 1 |
| `user_id` | integer | ID пользователя, оставившего отзыв | 5 |
| `user_name` | string \| null | Имя пользователя | "Иван Петров" |
| `rating` | integer | Рейтинг от 1 до 5 | 5 |
| `comment` | string \| null | Текст отзыва | "Отличный ресторан!" |
| `created_at` | datetime | Дата и время создания отзыва (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Пользовательские эндпоинты

### POST /api/v1/restaurants/
Создание нового ресторана (требует модерации)

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "name": "Ресторан Плов",
  "address": "Навои, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@restaurant.uz",
  "website": "https://restaurant.uz",
  "is_24_7": false,
  "working_hours": "09:00-23:00",
  "cuisine_type": "Узбекская",
  "average_check": 50000,
  "has_booking": true,
  "has_delivery": true,
  "has_parking": true,
  "has_wifi": true,
  "category": "Ресторан",
  "description": "Уютный ресторан с традиционной узбекской кухней",
  "menu_categories": [
    {
      "name": "Супы",
      "description": "Горячие супы",
      "order": 0,
      "items": [
        {
          "name": "Лагман",
          "description": "Традиционный лагман с лапшой и овощами",
          "price": 35000,
          "weight": "400г",
          "calories": 380,
          "order": 0
        }
      ]
    },
    {
      "name": "Горячие блюда",
      "description": "Основные блюда",
      "order": 1,
      "items": [
        {
          "name": "Плов",
          "description": "Традиционный узбекский плов с мясом",
          "price": 45000,
          "weight": "300г",
          "calories": 450,
          "order": 0
        }
      ]
    }
  ]
}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "name": "Ресторан Плов",
  "address": "Навои, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@restaurant.uz",
  "website": "https://restaurant.uz",
  "is_24_7": false,
  "working_hours": "09:00-23:00",
  "cuisine_type": "Узбекская",
  "average_check": 50000.0,
  "has_booking": true,
  "has_delivery": true,
  "has_parking": true,
  "has_wifi": true,
  "category": "Ресторан",
  "description": "Уютный ресторан с традиционной узбекской кухней",
  "rating": 0.0,
  "reviews_count": 0,
  "status": "pending",
  "has_promotions": false,
  "menu_categories": [
    {
      "id": 1,
      "restaurant_id": 1,
      "name": "Супы",
      "description": "Горячие супы",
      "order": 0,
      "items": [
        {
          "id": 1,
          "category_id": 1,
          "restaurant_id": 1,
          "name": "Лагман",
          "description": "Традиционный лагман с лапшой и овощами",
          "price": 35000.0,
          "image_url": null,
          "is_available": true,
          "weight": "400г",
          "calories": 380,
          "order": 0,
          "created_at": "2026-01-06T09:26:11.879Z",
          "updated_at": null
        }
      ],
      "created_at": "2026-01-06T09:26:11.879Z",
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

### GET /api/v1/restaurants/
Получение списка ресторанов с фильтрацией

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)
- `cuisine_type` - Тип кухни (см. Типы кухни)
- `min_rating` - Минимальный рейтинг (0-5)
- `min_average_check` - Минимальный средний чек
- `max_average_check` - Максимальный средний чек
- `is_24_7` - Работает 24/7 (true/false)
- `has_promotions` - Есть акции (true/false)
- `has_booking` - Есть бронирование (true/false)
- `has_delivery` - Есть доставка (true/false)
- `has_parking` - Есть парковка (true/false)
- `has_wifi` - Есть Wi-Fi (true/false)
- `search_query` - Поиск по названию, адресу или описанию
- `latitude` - Широта для поиска по близости
- `longitude` - Долгота для поиска по близости
- `radius_km` - Радиус поиска в километрах

**Пример:**
```
GET /api/v1/restaurants/?cuisine_type=Узбекская&min_rating=4.0&has_delivery=true&has_parking=true
```

**Ответ:**
```json
{
  "restaurants": [...],
  "total": 50,
  "skip": 0,
  "limit": 100
}
```

### GET /api/v1/restaurants/{restaurant_id}
Получение детальной информации о ресторане

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `restaurant_id` (integer, обязательный) - ID ресторана

**Ответ (200 OK):**
```json
{
  "id": 1,
  "name": "Ресторан Плов",
  "address": "Навои, 15, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@restaurant.uz",
  "website": "https://restaurant.uz",
  "is_24_7": false,
  "working_hours": "09:00-23:00",
  "cuisine_type": "Узбекская",
  "average_check": 50000.0,
  "has_booking": true,
  "has_delivery": true,
  "has_parking": true,
  "has_wifi": true,
  "category": "Ресторан",
  "description": "Уютный ресторан с традиционной узбекской кухней",
  "rating": 4.8,
  "reviews_count": 127,
  "status": "approved",
  "has_promotions": true,
  "menu_categories": [...],
  "photos": [...],
  "main_photo": "http://localhost:8000/uploads/restaurants/1_abc123.jpg",
  "reviews": [...],
  "created_at": "2026-01-06T09:26:11.879Z",
  "updated_at": "2026-01-06T10:15:30.123Z"
}
```

**Ошибки:**
- `404 Not Found` - Ресторан не найден или не одобрен
- `401 Unauthorized` - Требуется авторизация

### POST /api/v1/restaurants/{restaurant_id}/photos
Загрузка фотографии для ресторана

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры пути:**
- `restaurant_id` (integer, обязательный) - ID ресторана

**Параметры запроса (query):**
- `is_main` (boolean, опционально) - Главная фотография (по умолчанию false)
- `order` (integer, опционально) - Порядок отображения (по умолчанию 0, минимум 0)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения (разрешены: image/jpeg, image/jpg, image/png, image/webp, максимум 5MB)

**Ответ (201 Created):**
```json
{
  "id": 1,
  "restaurant_id": 1,
  "photo_url": "http://localhost:8000/uploads/restaurants/1_abc123.jpg",
  "is_main": true,
  "order": 0,
  "created_at": "2026-01-06T09:26:11.879Z"
}
```

**Ошибки:**
- `400 Bad Request` - Недопустимый тип файла или превышен размер
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Нет прав для добавления фотографий (только создатель или админ)
- `404 Not Found` - Ресторан не найден

### DELETE /api/v1/restaurants/{restaurant_id}/photos/{photo_id}
Удаление фотографии

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ (204 No Content):** Пустое тело ответа

### POST /api/v1/restaurants/{restaurant_id}/menu/categories
Создание категории меню

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос:**
```json
{
  "name": "Супы",
  "description": "Горячие супы",
  "order": 0,
  "items": [
    {
      "name": "Лагман",
      "description": "Традиционный лагман",
      "price": 35000,
      "weight": "400г",
      "calories": 380
    }
  ]
}
```

**Ответ (201 Created):** `MenuCategoryResponse`

### GET /api/v1/restaurants/{restaurant_id}/menu/categories
Получение всех категорий меню ресторана

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ (200 OK):** Массив `MenuCategoryResponse`

### PUT /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}
Обновление категории меню

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}
Удаление категории меню

**Требуется авторизация:** ✅ Да (Bearer token)

### POST /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}/items
Создание блюда в меню

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос:**
```json
{
  "name": "Плов",
  "description": "Традиционный узбекский плов",
  "price": 45000,
  "weight": "300г",
  "calories": 450,
  "is_available": true
}
```

**Ответ (201 Created):** `MenuItemResponse`

### GET /api/v1/restaurants/{restaurant_id}/menu/categories/{category_id}/items
Получение всех блюд категории

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ (200 OK):** Массив `MenuItemResponse`

### PUT /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}
Обновление блюда

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/restaurants/{restaurant_id}/menu/items/{item_id}
Удаление блюда

**Требуется авторизация:** ✅ Да (Bearer token)

### POST /api/v1/restaurants/{restaurant_id}/reviews
Создание отзыва о ресторане

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос:**
```json
{
  "rating": 5,
  "comment": "Отличный ресторан! Вкусная еда, быстрое обслуживание."
}
```

**Ответ (201 Created):** `RestaurantReviewResponse`

### PUT /api/v1/restaurants/{restaurant_id}/reviews/{review_id}
Обновление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/restaurants/{restaurant_id}/reviews/{review_id}
Удаление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

## Администраторские эндпоинты

### POST /api/v1/admin/restaurants/
Создание ресторана (сразу одобрен)

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

### GET /api/v1/admin/restaurants/
Получение списка всех ресторанов (включая ожидающие модерации)

**Параметры:**
- Все параметры из пользовательского эндпоинта
- `status` - Фильтр по статусу (pending, approved, rejected, archived)

### GET /api/v1/admin/restaurants/{restaurant_id}
Получение детальной информации о ресторане

### PUT /api/v1/admin/restaurants/{restaurant_id}
Обновление ресторана

**Запрос:**
```json
{
  "name": "Новое название",
  "has_promotions": true,
  "status": "approved"
}
```

### DELETE /api/v1/admin/restaurants/{restaurant_id}
Удаление ресторана

### POST /api/v1/admin/restaurants/{restaurant_id}/approve
Одобрение ресторана

### POST /api/v1/admin/restaurants/{restaurant_id}/reject
Отклонение ресторана

### POST /api/v1/admin/restaurants/{restaurant_id}/photos
Загрузка фотографии

### DELETE /api/v1/admin/restaurants/{restaurant_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/admin/restaurants/{restaurant_id}/photos/{photo_id}/set-main
Установка главной фотографии

### POST /api/v1/admin/restaurants/{restaurant_id}/menu/categories
Создание категории меню

### PUT /api/v1/admin/restaurants/{restaurant_id}/menu/categories/{category_id}
Обновление категории меню

### DELETE /api/v1/admin/restaurants/{restaurant_id}/menu/categories/{category_id}
Удаление категории меню

### POST /api/v1/admin/restaurants/{restaurant_id}/menu/categories/{category_id}/items
Создание блюда

### PUT /api/v1/admin/restaurants/{restaurant_id}/menu/items/{item_id}
Обновление блюда

### DELETE /api/v1/admin/restaurants/{restaurant_id}/menu/items/{item_id}
Удаление блюда

## Статусы ресторанов

| Статус | Описание | Видимость для пользователей |
|--------|----------|------------------------------|
| `pending` | Ожидает модерации (рестораны, созданные пользователями) | ❌ Не виден |
| `approved` | Одобрен администратором | ✅ Виден |
| `rejected` | Отклонен администратором | ❌ Не виден |
| `archived` | Архивирован (скрыт, но не удален) | ❌ Не виден |

**Примечание:** Пользователи видят только рестораны со статусом `approved`. Администраторы могут видеть и управлять всеми ресторанами.

## Типы кухни

Доступные типы кухни:
- `Узбекская` - Узбекская кухня
- `Русская` - Русская кухня
- `Европейская` - Европейская кухня
- `Азиатская` - Азиатская кухня
- `Итальянская` - Итальянская кухня
- `Японская` - Японская кухня
- `Китайская` - Китайская кухня
- `Американская` - Американская кухня
- `Фастфуд` - Фастфуд
- `Пицца` - Пицца
- `Суши` - Суши
- `Гриль` - Гриль
- `Вегетарианская` - Вегетарианская кухня
- `Другая` - Другая кухня

## Особенности

1. **Модерация**: Рестораны, созданные пользователями, автоматически получают статус `pending` и требуют одобрения админом. Рестораны, созданные админами, сразу получают статус `approved`.

2. **Рейтинг**: Автоматически пересчитывается при добавлении, изменении или удалении отзывов. Формула: среднее арифметическое всех рейтингов отзывов, округленное до 2 знаков после запятой.

3. **Главная фотография**: Можно установить одну главную фотографию для ресторана. При установке новой главной фотографии предыдущая автоматически перестает быть главной.

4. **Меню**: Структурированное меню с категориями и блюдами. Каждая категория может содержать несколько блюд. Блюда могут иметь фотографии, описание, цену, вес и калории.

5. **Фильтрация**: Поддерживается фильтрация по типу кухни, рейтингу, среднему чеку, режиму работы, наличию акций, дополнительным услугам (бронирование, доставка, парковка, Wi-Fi) и поиск по названию/адресу/описанию.

6. **Поиск по близости**: Можно искать рестораны в радиусе от указанных координат используя формулу гаверсинуса. Радиус указывается в километрах.

7. **Отзывы**: Один пользователь может оставить только один отзыв на ресторан. При повторной отправке отзыва существующий отзыв обновляется.

8. **Права доступа**: 
   - Пользователи могут создавать рестораны, добавлять фотографии и управлять меню только для своих ресторанов
   - Администраторы имеют полный доступ ко всем операциям

## Ограничения

- Максимальный размер файла фотографии: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка ресторанов в одном запросе: 1000 записей
- Рейтинг в отзывах: от 1 до 5 (целое число)
- Координаты: широта от -90 до 90, долгота от -180 до 180

## Примеры использования

### Создание ресторана пользователем
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ресторан Плов",
    "address": "Навои, 15, Tashkent",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "phone": "+998 90 123 45 67",
    "cuisine_type": "Узбекская",
    "average_check": 50000,
    "has_delivery": true,
    "has_parking": true
  }'
```

### Поиск ресторанов с фильтрацией
```bash
curl -X GET "http://localhost:8000/api/v1/restaurants/?cuisine_type=Узбекская&min_rating=4.0&has_delivery=true&has_parking=true" \
  -H "Authorization: Bearer <token>"
```

### Загрузка фотографии
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/1/photos?is_main=true" \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

### Создание категории меню
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/1/menu/categories" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Супы",
    "description": "Горячие супы",
    "items": [
      {
        "name": "Лагман",
        "description": "Традиционный лагман",
        "price": 35000,
        "weight": "400г"
      }
    ]
  }'
```

### Создание отзыва
```bash
curl -X POST "http://localhost:8000/api/v1/restaurants/1/reviews" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Отличный ресторан!"
  }'
```




