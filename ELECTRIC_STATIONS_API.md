# API для электрозаправок

## Описание

Система управления электрозаправками (зарядными станциями для электромобилей) с поддержкой:
- Добавления электрозаправок (пользователями и админами)
- Управления зарядными точками с различными типами разъемов
- Управления ценами на зарядку
- Загрузки фотографий
- Отзывов и рейтингов
- Фильтрации по различным параметрам
- Поиска по близости

## Модели данных

### ElectricStation (Электрозаправка)

#### Поля для создания/обновления (ElectricStationCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `name` | string | ✅ Да | Название электрозаправки (1-255 символов) | "Электрозаправка ПоЧо" |
| `address` | string | ✅ Да | Полный адрес электрозаправки (минимум 1 символ) | "Амира Темура, 25, Tashkent" |
| `latitude` | float | ✅ Да | Широта в градусах (-90 до 90) | 41.3111 |
| `longitude` | float | ✅ Да | Долгота в градусах (-180 до 180) | 69.2797 |
| `phone` | string | ❌ Нет | Номер телефона | "+998 90 123 45 67" |
| `email` | string | ❌ Нет | Email адрес | "info@electric.uz" |
| `website` | string | ❌ Нет | Сайт электрозаправки | "https://electric.uz" |
| `is_24_7` | boolean | ❌ Нет | Работает ли электрозаправка круглосуточно (по умолчанию false) | false |
| `working_hours` | string | ❌ Нет | Режим работы (если не 24/7) | "08:00-22:00" |
| `description` | string | ❌ Нет | Описание электрозаправки | "Современная зарядная станция" |
| `operator` | string | ❌ Нет | Оператор станции | "UzAuto Motors" |
| `network` | string | ❌ Нет | Сеть зарядных станций | "ChargePoint Network" |
| `has_parking` | boolean | ❌ Нет | Есть ли парковка (по умолчанию false) | true |
| `has_waiting_room` | boolean | ❌ Нет | Есть ли комната ожидания (по умолчанию false) | true |
| `has_cafe` | boolean | ❌ Нет | Есть ли кафе (по умолчанию false) | false |
| `has_restroom` | boolean | ❌ Нет | Есть ли туалет (по умолчанию false) | true |
| `accepts_cards` | boolean | ❌ Нет | Принимает ли карты (по умолчанию false) | true |
| `has_mobile_app` | boolean | ❌ Нет | Есть ли мобильное приложение (по умолчанию false) | true |
| `requires_membership` | boolean | ❌ Нет | Требуется ли членство (по умолчанию false) | false |
| `category` | string | ❌ Нет | Категория электрозаправки (по умолчанию "Электрозаправка") | "Электрозаправка" |
| `charging_points` | array | ❌ Нет | Массив зарядных точек (см. ChargingPointCreate) | см. ниже |

#### Поля в ответе (ElectricStationResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор электрозаправки | 1 |
| `name` | string | Название электрозаправки | "Электрозаправка ПоЧо" |
| `address` | string | Полный адрес электрозаправки | "Амира Темура, 25, Tashkent" |
| `latitude` | float | Широта в градусах | 41.3111 |
| `longitude` | float | Долгота в градусах | 69.2797 |
| `phone` | string \| null | Номер телефона | "+998 90 123 45 67" |
| `email` | string \| null | Email адрес | "info@electric.uz" |
| `website` | string \| null | Сайт электрозаправки | "https://electric.uz" |
| `is_24_7` | boolean | Работает ли электрозаправка круглосуточно | false |
| `working_hours` | string \| null | Режим работы | "08:00-22:00" |
| `description` | string \| null | Описание электрозаправки | "Современная зарядная станция" |
| `operator` | string \| null | Оператор станции | "UzAuto Motors" |
| `network` | string \| null | Сеть зарядных станций | "ChargePoint Network" |
| `has_parking` | boolean | Есть ли парковка | true |
| `has_waiting_room` | boolean | Есть ли комната ожидания | true |
| `has_cafe` | boolean | Есть ли кафе | false |
| `has_restroom` | boolean | Есть ли туалет | true |
| `accepts_cards` | boolean | Принимает ли карты | true |
| `has_mobile_app` | boolean | Есть ли мобильное приложение | true |
| `requires_membership` | boolean | Требуется ли членство | false |
| `category` | string | Категория электрозаправки | "Электрозаправка" |
| `total_points` | integer | Общее количество зарядных точек, автоматически обновляется | 4 |
| `available_points` | integer | Количество доступных точек, автоматически обновляется | 2 |
| `rating` | float | Средний рейтинг (0.0-5.0), автоматически рассчитывается | 4.8 |
| `reviews_count` | integer | Количество отзывов, автоматически обновляется | 127 |
| `status` | string | Статус электрозаправки: `pending`, `approved`, `rejected`, `archived` | "approved" |
| `has_promotions` | boolean | Есть ли акции/промо-предложения | true |
| `charging_points` | array | Массив зарядных точек (см. ChargingPointResponse) | см. ниже |
| `photos` | array | Массив фотографий электрозаправки (см. ElectricStationPhotoResponse) | см. ниже |
| `main_photo` | string \| null | URL главной фотографии электрозаправки | "http://localhost:8000/uploads/electric_stations/1_abc123.jpg" |
| `created_at` | datetime | Дата и время создания (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ChargingPoint (Зарядная точка)

#### Поля для создания/обновления (ChargingPointCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `connector_type` | enum | ✅ Да | Тип разъема (см. Типы разъемов) | "Type 2" |
| `power_kw` | float | ✅ Да | Мощность в кВт (должна быть больше 0) | 50.0 |
| `connector_name` | string | ❌ Нет | Название разъема (до 255 символов) | "Разъем 1" |
| `price_per_kwh` | float | ❌ Нет | Цена за кВт·ч в сумах (должна быть больше 0) | 2000.0 |
| `price_per_minute` | float | ❌ Нет | Цена за минуту в сумах (должна быть больше 0) | 500.0 |
| `min_price` | float | ❌ Нет | Минимальная плата в сумах (минимум 0) | 10000.0 |
| `status` | enum | ❌ Нет | Статус зарядной точки (по умолчанию `unknown`) | "available" |

#### Поля в ответе (ChargingPointResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор зарядной точки | 1 |
| `electric_station_id` | integer | ID электрозаправки | 1 |
| `connector_type` | string | Тип разъема | "Type 2" |
| `power_kw` | float | Мощность в кВт | 50.0 |
| `connector_name` | string \| null | Название разъема | "Разъем 1" |
| `price_per_kwh` | float \| null | Цена за кВт·ч в сумах | 2000.0 |
| `price_per_minute` | float \| null | Цена за минуту в сумах | 500.0 |
| `min_price` | float \| null | Минимальная плата в сумах | 10000.0 |
| `status` | string | Статус зарядной точки | "available" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ElectricStationPhoto (Фотография)

#### Поля для создания (ElectricStationPhotoCreate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `is_main` | boolean | ❌ Нет | Является ли фотография главной (по умолчанию false) | true |
| `order` | integer | ❌ Нет | Порядок отображения (по умолчанию 0) | 0 |

**Примечание:** Файл загружается через `multipart/form-data` с полем `file`.

#### Поля в ответе (ElectricStationPhotoResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор фотографии | 1 |
| `electric_station_id` | integer | ID электрозаправки | 1 |
| `photo_url` | string | Полный URL фотографии | "http://localhost:8000/uploads/electric_stations/1_abc123.jpg" |
| `is_main` | boolean | Является ли фотография главной | true |
| `order` | integer | Порядок отображения | 0 |
| `created_at` | datetime | Дата и время загрузки (ISO 8601) | "2026-01-06T09:26:11.879Z" |

### ElectricStationReview (Отзыв)

#### Поля для создания/обновления (ElectricStationReviewCreate/ElectricStationReviewUpdate):

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `rating` | integer | ✅ Да | Рейтинг от 1 до 5 | 5 |
| `comment` | string | ❌ Нет | Текст отзыва | "Отличная зарядная станция!" |
| `charging_speed_rating` | integer | ❌ Нет | Оценка скорости зарядки (1-5) | 5 |
| `price_rating` | integer | ❌ Нет | Оценка цены (1-5) | 4 |
| `location_rating` | integer | ❌ Нет | Оценка местоположения (1-5) | 5 |

#### Поля в ответе (ElectricStationReviewResponse):

| Поле | Тип | Описание | Пример |
|------|-----|----------|--------|
| `id` | integer | Уникальный идентификатор отзыва | 1 |
| `electric_station_id` | integer | ID электрозаправки | 1 |
| `user_id` | integer | ID пользователя, оставившего отзыв | 5 |
| `user_name` | string \| null | Имя пользователя | "Иван Петров" |
| `rating` | integer | Рейтинг от 1 до 5 | 5 |
| `comment` | string \| null | Текст отзыва | "Отличная зарядная станция!" |
| `charging_speed_rating` | integer \| null | Оценка скорости зарядки (1-5) | 5 |
| `price_rating` | integer \| null | Оценка цены (1-5) | 4 |
| `location_rating` | integer \| null | Оценка местоположения (1-5) | 5 |
| `created_at` | datetime | Дата и время создания отзыва (ISO 8601) | "2026-01-06T09:26:11.879Z" |
| `updated_at` | datetime \| null | Дата и время последнего обновления (ISO 8601) | "2026-01-06T09:26:11.879Z" |

## Пользовательские эндпоинты

### POST /api/v1/electric-stations/
Создание новой электрозаправки (требует модерации)

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос (Content-Type: application/json):**
```json
{
  "name": "Электрозаправка ПоЧо",
  "address": "Амира Темура, 25, Tashkent",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998 90 123 45 67",
  "email": "info@electric.uz",
  "is_24_7": false,
  "working_hours": "08:00-22:00",
  "description": "Современная зарядная станция",
  "operator": "UzAuto Motors",
  "network": "ChargePoint Network",
  "has_parking": true,
  "has_waiting_room": true,
  "has_restroom": true,
  "accepts_cards": true,
  "has_mobile_app": true,
  "requires_membership": false,
  "charging_points": [
    {
      "connector_type": "Type 2",
      "power_kw": 50.0,
      "connector_name": "Разъем 1",
      "price_per_kwh": 2000.0,
      "min_price": 10000.0,
      "status": "available"
    },
    {
      "connector_type": "CCS Type 2",
      "power_kw": 150.0,
      "connector_name": "Разъем 2",
      "price_per_kwh": 2500.0,
      "min_price": 15000.0,
      "status": "available"
    }
  ]
}
```

**Ответ (201 Created):** `ElectricStationResponse`

### GET /api/v1/electric-stations/
Получение списка электрозаправок с фильтрацией

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры запроса:**
- `skip` - Пропустить записей (по умолчанию 0)
- `limit` - Лимит записей (по умолчанию 100, максимум 1000)
- `connector_type` - Тип разъема (см. Типы разъемов)
- `min_power_kw` - Минимальная мощность в кВт
- `max_power_kw` - Максимальная мощность в кВт
- `min_price_per_kwh` - Минимальная цена за кВт·ч
- `max_price_per_kwh` - Максимальная цена за кВт·ч
- `min_rating` - Минимальный рейтинг (0-5)
- `is_24_7` - Работает 24/7 (true/false)
- `has_promotions` - Есть акции (true/false)
- `has_parking` - Есть парковка (true/false)
- `has_waiting_room` - Есть комната ожидания (true/false)
- `has_cafe` - Есть кафе (true/false)
- `has_restroom` - Есть туалет (true/false)
- `accepts_cards` - Принимает карты (true/false)
- `has_mobile_app` - Есть мобильное приложение (true/false)
- `requires_membership` - Требуется членство (true/false)
- `has_available_points` - Есть свободные точки (true/false)
- `operator` - Фильтр по оператору
- `network` - Фильтр по сети
- `search_query` - Поиск по названию, адресу или описанию
- `latitude` - Широта для поиска по близости
- `longitude` - Долгота для поиска по близости
- `radius_km` - Радиус поиска в километрах

**Пример:**
```
GET /api/v1/electric-stations/?connector_type=Type 2&min_power_kw=50&has_parking=true&has_available_points=true
```

**Ответ:** `ElectricStationListResponse`

### GET /api/v1/electric-stations/{station_id}
Получение детальной информации об электрозаправке

**Требуется авторизация:** ✅ Да (Bearer token)

**Ответ:** `ElectricStationDetailResponse` (включает отзывы)

### POST /api/v1/electric-stations/{station_id}/photos
Загрузка фотографии для электрозаправки

**Требуется авторизация:** ✅ Да (Bearer token)

**Параметры запроса (query):**
- `is_main` (boolean, опционально) - Главная фотография (по умолчанию false)
- `order` (integer, опционально) - Порядок отображения (по умолчанию 0, минимум 0)

**Тело запроса (multipart/form-data):**
- `file` (file, обязательный) - Файл изображения

**Ответ (201 Created):** `ElectricStationPhotoResponse`

### DELETE /api/v1/electric-stations/{station_id}/photos/{photo_id}
Удаление фотографии

**Требуется авторизация:** ✅ Да (Bearer token)

### POST /api/v1/electric-stations/{station_id}/charging-points
Обновление зарядных точек электрозаправки

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос:** `BulkChargingPointUpdate`
```json
{
  "charging_points": [
    {
      "connector_type": "Type 2",
      "power_kw": 50.0,
      "connector_name": "Разъем 1",
      "price_per_kwh": 2000.0,
      "status": "available"
    }
  ]
}
```

**Ответ:** Список обновленных зарядных точек (`List[ChargingPointResponse]`)

### POST /api/v1/electric-stations/{station_id}/reviews
Создание отзыва об электрозаправке

**Требуется авторизация:** ✅ Да (Bearer token)

**Запрос:** `ElectricStationReviewCreate`
```json
{
  "rating": 5,
  "comment": "Отличная зарядная станция!",
  "charging_speed_rating": 5,
  "price_rating": 4,
  "location_rating": 5
}
```

**Ответ (201 Created):** `ElectricStationReviewResponse`

### PUT /api/v1/electric-stations/{station_id}/reviews/{review_id}
Обновление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

### DELETE /api/v1/electric-stations/{station_id}/reviews/{review_id}
Удаление отзыва

**Требуется авторизация:** ✅ Да (Bearer token)

## Администраторские эндпоинты

### POST /api/v1/admin/electric-stations/
Создание электрозаправки (сразу одобрена)

**Требуется авторизация:** ✅ Да (только админ, Bearer token)

### GET /api/v1/admin/electric-stations/
Получение списка всех электрозаправок (включая ожидающие модерации)

**Параметры:** Все параметры из пользовательского эндпоинта + `status` - Фильтр по статусу

### GET /api/v1/admin/electric-stations/{station_id}
Получение детальной информации об электрозаправке

### PUT /api/v1/admin/electric-stations/{station_id}
Обновление электрозаправки

### DELETE /api/v1/admin/electric-stations/{station_id}
Удаление электрозаправки

### POST /api/v1/admin/electric-stations/{station_id}/approve
Одобрение электрозаправки

### POST /api/v1/admin/electric-stations/{station_id}/reject
Отклонение электрозаправки

### POST /api/v1/admin/electric-stations/{station_id}/photos
Загрузка фотографии

### DELETE /api/v1/admin/electric-stations/{station_id}/photos/{photo_id}
Удаление фотографии

### POST /api/v1/admin/electric-stations/{station_id}/photos/{photo_id}/set-main
Установка главной фотографии

### POST /api/v1/admin/electric-stations/{station_id}/charging-points
Обновление зарядных точек

## Статусы электрозаправок

| Статус | Описание | Видимость для пользователей |
|--------|----------|------------------------------|
| `pending` | Ожидает модерации (электрозаправки, созданные пользователями) | ❌ Не видна |
| `approved` | Одобрена администратором | ✅ Видна |
| `rejected` | Отклонена администратором | ❌ Не видна |
| `archived` | Архивирована (скрыта, но не удалена) | ❌ Не видна |

## Типы зарядных разъемов

Доступные типы разъемов:
- `Type 1` - SAE J1772 (стандарт для Северной Америки и Японии)
- `Type 2` - Mennekes (IEC 62196, стандарт для Европы)
- `CCS Type 1` - Combo 1 (быстрая зарядка, Северная Америка)
- `CCS Type 2` - Combo 2 (быстрая зарядка, Европа)
- `CHAdeMO` - Японский стандарт быстрой зарядки
- `Tesla Supercharger` - Сеть быстрых зарядок Tesla
- `Tesla Destination` - Медленные зарядки Tesla
- `GB/T` - Китайский стандарт
- `Другое` - Другие типы разъемов

## Статусы зарядных точек

| Статус | Описание |
|--------|----------|
| `available` | Доступна для зарядки |
| `occupied` | Занята (в данный момент используется) |
| `out_of_order` | Неисправна (не работает) |
| `unknown` | Статус неизвестен |

## Особенности

1. **Модерация**: Электрозаправки, созданные пользователями, автоматически получают статус `pending` и требуют одобрения админом. Электрозаправки, созданные админами, сразу получают статус `approved`.

2. **Рейтинг**: Автоматически пересчитывается при добавлении, изменении или удалении отзывов. Формула: среднее арифметическое всех рейтингов отзывов, округленное до 2 знаков после запятой.

3. **Зарядные точки**: Можно указать несколько зарядных точек с разными типами разъемов, мощностями и ценами. Система автоматически обновляет счетчики `total_points` и `available_points`.

4. **Ценообразование**: Поддерживается два типа ценообразования:
   - По кВт·ч (`price_per_kwh`)
   - По времени (`price_per_minute`)
   - Можно указать минимальную плату (`min_price`)

5. **Фильтрация**: Поддерживается фильтрация по типу разъема, мощности, цене, рейтингу, режиму работы, наличию акций, дополнительным услугам (парковка, комната ожидания, кафе, туалет, прием карт, мобильное приложение, членство), наличию свободных точек, оператору, сети и поиск по названию/адресу/описанию.

6. **Поиск по близости**: Можно искать электрозаправки в радиусе от указанных координат используя формулу гаверсинуса. Радиус указывается в километрах.

7. **Отзывы**: Один пользователь может оставить только один отзыв на электрозаправку. При повторной отправке отзыва существующий отзыв обновляется. Поддерживаются дополнительные оценки: скорость зарядки, цена, местоположение.

8. **Права доступа**: 
   - Пользователи могут создавать электрозаправки, добавлять фотографии и обновлять зарядные точки только для своих электрозаправок
   - Администраторы имеют полный доступ ко всем операциям

## Ограничения

- Максимальный размер файла фотографии: 5MB
- Разрешенные типы изображений: JPEG, JPG, PNG, WebP
- Максимальная длина списка электрозаправок в одном запросе: 1000 записей
- Рейтинг в отзывах: от 1 до 5 (целое число)
- Координаты: широта от -90 до 90, долгота от -180 до 180
- Мощность зарядки: должна быть больше 0 кВт

## Примеры использования

### Создание электрозаправки пользователем
```bash
curl -X POST "http://localhost:8000/api/v1/electric-stations/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Электрозаправка ПоЧо",
    "address": "Амира Темура, 25, Tashkent",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "has_parking": true,
    "has_waiting_room": true,
    "has_restroom": true,
    "accepts_cards": true,
    "charging_points": [
      {
        "connector_type": "Type 2",
        "power_kw": 50.0,
        "price_per_kwh": 2000.0,
        "status": "available"
      }
    ]
  }'
```

### Поиск электрозаправок с фильтрацией
```bash
curl -X GET "http://localhost:8000/api/v1/electric-stations/?connector_type=Type 2&min_power_kw=50&has_parking=true&has_available_points=true" \
  -H "Authorization: Bearer <token>"
```

### Загрузка фотографии
```bash
curl -X POST "http://localhost:8000/api/v1/electric-stations/1/photos?is_main=true" \
  -H "Authorization: Bearer <token>" \
  -F "file=@photo.jpg"
```

### Обновление зарядных точек
```bash
curl -X POST "http://localhost:8000/api/v1/electric-stations/1/charging-points" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "charging_points": [
      {
        "connector_type": "Type 2",
        "power_kw": 50.0,
        "connector_name": "Разъем 1",
        "price_per_kwh": 2000.0,
        "status": "available"
      },
      {
        "connector_type": "CCS Type 2",
        "power_kw": 150.0,
        "connector_name": "Разъем 2",
        "price_per_kwh": 2500.0,
        "status": "available"
      }
    ]
  }'
```

### Создание отзыва
```bash
curl -X POST "http://localhost:8000/api/v1/electric-stations/1/reviews" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Отличная зарядная станция!",
    "charging_speed_rating": 5,
    "price_rating": 4,
    "location_rating": 5
  }'
```

