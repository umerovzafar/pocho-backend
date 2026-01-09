# API Статистики Администратора

API для получения статистики и аналитики для администраторского дашборда.

## Базовый URL

```
/api/v1/admin/statistics
```

## Аутентификация

Все эндпоинты требуют прав администратора. Используйте JWT токен в заголовке:

```
Authorization: Bearer <admin_token>
```

---

## Эндпоинты

### 1. Получение полного дашборда

**GET** `/dashboard`

Возвращает все данные для отображения дашборда администратора.

#### Параметры запроса (Query)

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода
- `period_days` (optional, int, default=7): Количество дней для периода (1-365)

#### Пример запроса

```bash
GET /api/v1/admin/statistics/dashboard?period_days=7
```

#### Пример ответа

```json
{
  "kpis": {
    "total_users": {
      "value": 12543,
      "change_percent": 2.5,
      "change_value": 1234,
      "period_value": 1234
    },
    "active_users": {
      "value": 8921,
      "change_percent": 0.2,
      "change_value": 200,
      "period_value": 200
    },
    "total_requests": {
      "value": 130,
      "change_percent": 3.0,
      "change_value": 3,
      "period_value": 127
    },
    "revenue": {
      "value": 18750000,
      "change_percent": 15.3,
      "change_value": 1875000,
      "period_value": 1875000
    }
  },
  "category_metrics": {
    "gas_stations": {
      "total": 214,
      "active": 200,
      "change": 13
    },
    "restaurants": {
      "total": 71,
      "active": 67,
      "change": 4
    },
    "service_stations": {
      "total": 47,
      "active": 45,
      "change": 2
    },
    "car_washes": {
      "total": 94,
      "active": 89,
      "change": 3
    },
    "electric_stations": {
      "total": 41,
      "active": 22,
      "change": 1
    }
  },
  "revenue_chart": {
    "labels": ["1д", "2д", "3д", "4д", "5д", "6д", "7д"],
    "revenue": [2500000, 3000000, 2800000, 3200000, 2900000, 3100000, 3050000],
    "orders": [25, 30, 28, 32, 29, 31, 30]
  },
  "new_users_chart": {
    "labels": ["1д", "2д", "3д", "4д", "5д", "6д", "7д"],
    "users": [150, 180, 165, 200, 175, 190, 185]
  },
  "user_activity_chart": {
    "labels": ["00:00", "06:00", "12:00", "18:00", "24:00"],
    "activity": [100, 500, 3000, 2500, 800]
  },
  "category_distribution": {
    "categories": [
      {
        "category": "Рестораны",
        "count": 67,
        "percentage": 28.5,
        "color": "#ef4444"
      },
      {
        "category": "Заправки",
        "count": 200,
        "percentage": 85.1,
        "color": "#ec4899"
      },
      {
        "category": "СТО",
        "count": 45,
        "percentage": 19.1,
        "color": "#10b981"
      },
      {
        "category": "Автомойки",
        "count": 89,
        "percentage": 37.9,
        "color": "#06b6d4"
      },
      {
        "category": "Электрозаправки",
        "count": 22,
        "percentage": 9.4,
        "color": "#3b82f6"
      }
    ]
  },
  "latest_transactions": {
    "transactions": [
      {
        "id": 1,
        "user_name": "Иван Иванов",
        "user_phone": "+998900000001",
        "type": "Заправки",
        "amount": 45000,
        "status": "Завершено",
        "created_at": "2026-01-08T10:30:00Z"
      },
      {
        "id": 2,
        "user_name": "Али Алина",
        "user_phone": "+998900000002",
        "type": "Рестораны",
        "amount": 125000,
        "status": "В обработке",
        "created_at": "2026-01-08T09:15:00Z"
      }
    ],
    "total": 234
  },
  "category_completeness": {
    "categories": [
      {
        "category": "Заправки",
        "current": 200,
        "target": 150,
        "percentage": 133.3
      },
      {
        "category": "Рестораны",
        "current": 67,
        "target": 100,
        "percentage": 67.0
      },
      {
        "category": "СТО",
        "current": 45,
        "target": 60,
        "percentage": 75.0
      },
      {
        "category": "Автомойки",
        "current": 89,
        "target": 80,
        "percentage": 111.3
      },
      {
        "category": "Электрозаправки",
        "current": 22,
        "target": 40,
        "percentage": 55.0
      }
    ]
  },
  "recent_actions": {
    "actions": [
      {
        "id": 1,
        "action_type": "user_registered",
        "description": "Новый пользователь зарегистрирован: Иван Иванов",
        "created_at": "2026-01-08T10:00:00Z",
        "time_ago": "2 минуты назад"
      },
      {
        "id": 2,
        "action_type": "gas_station_added",
        "description": "Добавлена новая заправка: Petrol Exclusive",
        "created_at": "2026-01-08T09:45:00Z",
        "time_ago": "15 минут назад"
      }
    ],
    "total": 5
  },
  "order_statistics": {
    "total_orders": 234,
    "statuses": [
      {
        "status": "Завершено",
        "count": 180,
        "percentage": 76.9
      },
      {
        "status": "В обработке",
        "count": 28,
        "percentage": 12.0
      },
      {
        "status": "Отменено",
        "count": 6,
        "percentage": 2.6
      }
    ]
  },
  "system_activity": {
    "total_activity": {
      "value": 3421,
      "change_percent": 1.2,
      "change_value": 40
    },
    "average_check": {
      "value": 53419,
      "change_percent": 1.2,
      "change_value": 650
    },
    "conversion": 27.3,
    "satisfaction": 4.7
  }
}
```

---

### 2. Получение KPI показателей

**GET** `/kpis`

Возвращает основные KPI показатели.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода
- `period_days` (optional, int, default=7): Количество дней для периода

#### Пример ответа

```json
{
  "total_users": {
    "value": 12543,
    "change_percent": 2.5,
    "change_value": 1234,
    "period_value": 1234
  },
  "active_users": {
    "value": 8921,
    "change_percent": 0.2,
    "change_value": 200,
    "period_value": 200
  },
  "total_requests": {
    "value": 130,
    "change_percent": 3.0,
    "change_value": 3,
    "period_value": 127
  },
  "revenue": {
    "value": 18750000,
    "change_percent": 15.3,
    "change_value": 1875000,
    "period_value": 1875000
  }
}
```

---

### 3. Получение метрик по категориям

**GET** `/category-metrics`

Возвращает метрики по категориям (заправки, рестораны, СТО, автомойки, электрозаправки).

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода

#### Пример ответа

```json
{
  "gas_stations": {
    "total": 214,
    "active": 200,
    "change": 13
  },
  "restaurants": {
    "total": 71,
    "active": 67,
    "change": 4
  },
  "service_stations": {
    "total": 47,
    "active": 45,
    "change": 2
  },
  "car_washes": {
    "total": 94,
    "active": 89,
    "change": 3
  },
  "electric_stations": {
    "total": 41,
    "active": 22,
    "change": 1
  }
}
```

---

### 4. Получение графика выручки

**GET** `/revenue-chart`

Возвращает данные для графика выручки.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода
- `period_days` (optional, int, default=7): Количество дней для периода

#### Пример ответа

```json
{
  "labels": ["1д", "2д", "3д", "4д", "5д", "6д", "7д"],
  "revenue": [2500000, 3000000, 2800000, 3200000, 2900000, 3100000, 3050000],
  "orders": [25, 30, 28, 32, 29, 31, 30]
}
```

---

### 5. Получение графика новых пользователей

**GET** `/new-users-chart`

Возвращает данные для графика новых пользователей.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода
- `period_days` (optional, int, default=7): Количество дней для периода

#### Пример ответа

```json
{
  "labels": ["1д", "2д", "3д", "4д", "5д", "6д", "7д"],
  "users": [150, 180, 165, 200, 175, 190, 185]
}
```

---

### 6. Получение графика активности пользователей

**GET** `/user-activity-chart`

Возвращает данные для графика активности пользователей по часам дня.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода

#### Пример ответа

```json
{
  "labels": ["00:00", "01:00", "02:00", ..., "23:00"],
  "activity": [100, 80, 50, ..., 120]
}
```

---

### 7. Получение распределения по категориям

**GET** `/category-distribution`

Возвращает распределение объектов по категориям (для круговой диаграммы).

#### Пример ответа

```json
{
  "categories": [
    {
      "category": "Рестораны",
      "count": 67,
      "percentage": 28.5,
      "color": "#ef4444"
    },
    {
      "category": "Заправки",
      "count": 200,
      "percentage": 85.1,
      "color": "#ec4899"
    }
  ]
}
```

---

### 8. Получение последних транзакций

**GET** `/latest-transactions`

Возвращает список последних транзакций.

#### Параметры запроса

- `limit` (optional, int, default=5, max=100): Количество транзакций

#### Пример ответа

```json
{
  "transactions": [
    {
      "id": 1,
      "user_name": "Иван Иванов",
      "user_phone": "+998900000001",
      "type": "Заправки",
      "amount": 45000,
      "status": "Завершено",
      "created_at": "2026-01-08T10:30:00Z"
    }
  ],
  "total": 234
}
```

---

### 9. Получение заполненности категорий

**GET** `/category-completeness`

Возвращает информацию о заполненности категорий (текущее количество vs целевое).

#### Пример ответа

```json
{
  "categories": [
    {
      "category": "Заправки",
      "current": 200,
      "target": 150,
      "percentage": 133.3
    },
    {
      "category": "Рестораны",
      "current": 67,
      "target": 100,
      "percentage": 67.0
    }
  ]
}
```

---

### 10. Получение последних действий

**GET** `/recent-actions`

Возвращает список последних действий в системе.

#### Параметры запроса

- `limit` (optional, int, default=5, max=100): Количество действий

#### Пример ответа

```json
{
  "actions": [
    {
      "id": 1,
      "action_type": "user_registered",
      "description": "Новый пользователь зарегистрирован: Иван Иванов",
      "created_at": "2026-01-08T10:00:00Z",
      "time_ago": "2 минуты назад"
    }
  ],
  "total": 5
}
```

---

### 11. Получение статистики заказов

**GET** `/order-statistics`

Возвращает статистику заказов по статусам.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода

#### Пример ответа

```json
{
  "total_orders": 234,
  "statuses": [
    {
      "status": "Завершено",
      "count": 180,
      "percentage": 76.9
    },
    {
      "status": "В обработке",
      "count": 28,
      "percentage": 12.0
    },
    {
      "status": "Отменено",
      "count": 6,
      "percentage": 2.6
    }
  ]
}
```

---

### 12. Получение активности системы

**GET** `/system-activity`

Возвращает общую активность системы.

#### Параметры запроса

- `start_date` (optional, datetime): Начальная дата периода
- `end_date` (optional, datetime): Конечная дата периода

#### Пример ответа

```json
{
  "total_activity": {
    "value": 3421,
    "change_percent": 1.2,
    "change_value": 40
  },
  "average_check": {
    "value": 53419,
    "change_percent": 1.2,
    "change_value": 650
  },
  "conversion": 27.3,
  "satisfaction": 4.7
}
```

---

## Типы данных

### KPIValue

```json
{
  "value": 12543,
  "change_percent": 2.5,
  "change_value": 1234,
  "period_value": 1234
}
```

- `value`: Текущее значение
- `change_percent`: Процент изменения (может быть null)
- `change_value`: Абсолютное изменение (может быть null)
- `period_value`: Значение за период (может быть null)

### CategoryMetric

```json
{
  "total": 214,
  "active": 200,
  "change": 13
}
```

- `total`: Общее количество
- `active`: Количество активных (одобренных)
- `change`: Изменение за период

---

## Ошибки

### 401 Unauthorized

Требуется аутентификация администратора.

```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden

Недостаточно прав доступа.

```json
{
  "detail": "Access denied. Admin rights required."
}
```

### 500 Internal Server Error

Внутренняя ошибка сервера.

```json
{
  "detail": "Произошла ошибка при получении данных дашборда"
}
```

---

## Примечания

1. Все даты и время в формате ISO 8601 (UTC)
2. Проценты изменения рассчитываются относительно предыдущего периода
3. Графики автоматически группируются по часам (для периода ≤ 1 дня) или по дням (для периода > 1 дня)
4. Целевые значения для заполненности категорий можно настроить в коде
5. Все суммы в сумах (UZS)



