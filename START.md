# Инструкция по запуску проекта

## Быстрый старт

### Вариант 1: Использование run.py (рекомендуется)

**В Git Bash:**
```bash
# Активируйте виртуальное окружение
source venv/Scripts/activate

# Запустите проект
python run.py
```

**В Windows CMD:**
```cmd
venv\Scripts\activate
python run.py
```

**В PowerShell:**
```powershell
venv\Scripts\Activate.ps1
python run.py
```

### Вариант 2: Использование uvicorn напрямую

**В Git Bash:**
```bash
source venv/Scripts/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**В Windows CMD:**
```cmd
venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**В PowerShell:**
```powershell
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## После запуска

Приложение будет доступно по адресам:
- **API**: http://localhost:8000
- **Swagger документация**: http://localhost:8000/docs
- **ReDoc документация**: http://localhost:8000/redoc

## Важные замечания

1. **Убедитесь, что PostgreSQL запущен** и база данных создана
2. **Проверьте файл `.env`** - должны быть настроены:
   - `DATABASE_URL` - подключение к PostgreSQL
   - `SECRET_KEY` - секретный ключ для JWT
   - `SMS_API_URL` - URL SMS API (если используете SMS)
   - `SMS_API_TOKEN` - токен для SMS API

## Решение проблем

### Ошибка "python: command not found"
Используйте `py` вместо `python`:
```bash
py run.py
```

### Ошибка "uvicorn: command not found"
Убедитесь, что виртуальное окружение активировано:
```bash
source venv/Scripts/activate
pip install -r requirements.txt
```

### Ошибка подключения к базе данных
Проверьте:
1. PostgreSQL запущен
2. База данных `pocho_db` создана
3. `DATABASE_URL` в `.env` правильный_


