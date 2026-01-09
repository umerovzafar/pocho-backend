# Формат .env файла

Убедитесь, что ваш `.env` файл имеет правильный формат:

## Правильный формат:

```env
DATABASE_URL=postgresql://postgres:24032001@localhost:5433/pocho_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_PREFIX=/api/v1
CORS_ORIGINS=*
```

## Важные правила:

1. **НЕ используйте пробелы вокруг знака `=`**
   - ✅ Правильно: `DATABASE_URL=value`
   - ❌ Неправильно: `DATABASE_URL = value`

2. **НЕ используйте кавычки** (если значение не содержит пробелов)
   - ✅ Правильно: `SECRET_KEY=my-secret-key`
   - ❌ Неправильно: `SECRET_KEY="my-secret-key"`

3. **НЕ дублируйте переменные** - каждая переменная должна быть указана только один раз

4. **Комментарии** начинаются с `#`

5. **Пустые строки** игнорируются

## Пример правильного .env файла:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:24032001@localhost:5433/pocho_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_PREFIX=/api/v1

# CORS Configuration
CORS_ORIGINS=*
```

## Проверка:

Запустите скрипт проверки:
```bash
python check_config.py
```

Если значения не загружаются, проверьте:
- Файл находится в корне проекта (рядом с `app/` папкой)
- Нет дубликатов переменных
- Нет пробелов вокруг `=`
- Файл сохранен в кодировке UTF-8




