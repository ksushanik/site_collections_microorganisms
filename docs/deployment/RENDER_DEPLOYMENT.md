# 🚀 Развертывание проекта СИФИБР на Render.com

## Обзор

Проект СИФИБР развертывается на Render.com с использованием следующих сервисов:
- **Backend**: Django Web Service (gunicorn)
- **Frontend**: React Static Site
- **Database**: PostgreSQL Database

## Подготовка проекта

### 1. GitHub репозиторий
Убедитесь, что проект загружен на GitHub:

```bash
git add .
git commit -m "feat: подготовка к деплою на Render"
git push origin main
```

### 2. Файлы конфигурации
Проект уже содержит необходимые файлы:
- `render.yaml` - автоматическая конфигурация Render
- `build.sh` - скрипт сборки для Django
- Обновленные настройки CORS и production

## Развертывание

### Автоматический деплой через render.yaml

1. **Войдите в Render Dashboard**: https://dashboard.render.com/
2. **Создайте новый Blueprint**: New → Blueprint
3. **Подключите GitHub**: Авторизуйтесь и выберите репозиторий
4. **Render автоматически найдет** `render.yaml` и создаст все сервисы

### Ручное развертывание

#### Шаг 1: PostgreSQL Database

1. **New → PostgreSQL**
2. **Name**: `sifibr-db`
3. **Database Name**: `sifibr_collections`
4. **User**: `sifibr`
5. **Region**: Oregon (US West)
6. **Plan**: Free
7. **Create Database**

#### Шаг 2: Django Backend

1. **New → Web Service**
2. **Connect Repository**: Выберите ваш GitHub репо
3. **Settings**:
   - **Name**: `sifibr-backend`
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install --upgrade pip
     pip install -r requirements.txt
     python manage.py collectstatic --noinput
     python manage.py migrate
     ```
   - **Start Command**:
     ```bash
     python manage.py create_test_data
     gunicorn sifibr_collections.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Health Check Path**: `/api/health/`

4. **Environment Variables**:
   ```
   DEBUG=False
   ALLOWED_HOSTS=sifibr-backend.onrender.com,localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=https://sifibr-frontend.onrender.com,http://localhost:3000
   SECRET_KEY=[auto-generated]
   DATABASE_URL=[auto-connected to database]
   RENDER=true
   DJANGO_SETTINGS_MODULE=sifibr_collections.settings
   ```

#### Шаг 3: React Frontend

1. **New → Static Site**
2. **Connect Repository**: Тот же репо
3. **Settings**:
   - **Name**: `sifibr-frontend`
   - **Build Command**:
     ```bash
     cd frontend
     npm ci
     npm run build
     ```
   - **Publish Directory**: `frontend/dist`

4. **Environment Variables**:
   ```
   VITE_API_URL=https://sifibr-backend.onrender.com
   ```

## Проверка развертывания

### Backend Health Check
```bash
curl https://sifibr-backend.onrender.com/api/health/
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "database": "connected",
  "collections_count": 5,
  "strains_count": 7
}
```

### Frontend
- Откройте: https://sifibr-frontend.onrender.com
- Должен загрузиться интерфейс с данными
- Проверьте работу каталога и поиска

### Django Admin
- Откройте: https://sifibr-backend.onrender.com/admin/
- Логин: `admin`
- Пароль: `sifibr_admin_2025`

## Устранение неполадок

### Проблемы с базой данных
```bash
# Проверьте логи backend сервиса
# В Render Dashboard → sifibr-backend → Logs

# Проверьте подключение к БД
python manage.py dbshell
```

### Проблемы с CORS
```python
# Добавьте в CORS_ALLOWED_ORIGINS в settings.py:
CORS_ALLOWED_ORIGINS = [
    "https://your-actual-frontend-url.onrender.com",
    "https://your-actual-backend-url.onrender.com",
]
```

### Проблемы со статическими файлами
```bash
# Пересоберите статику
python manage.py collectstatic --noinput --clear
```

### Timeout ошибки
```python
# Увеличьте timeout в gunicorn
gunicorn sifibr_collections.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
```

## Мониторинг

### Логи
- **Backend**: Render Dashboard → sifibr-backend → Logs
- **Frontend**: Render Dashboard → sifibr-frontend → Logs
- **Database**: Render Dashboard → sifibr-db → Logs

### Метрики
- **Performance**: Render автоматически предоставляет метрики
- **Health checks**: /api/health/ endpoint
- **Uptime**: Render monitoring dashboard

## Обновления

### Автоматические обновления
Render автоматически пересобирает при push в main:

```bash
git add .
git commit -m "feat: новая функциональность"
git push origin main
```

### Ручные обновления
1. Render Dashboard → Service → Manual Deploy
2. Или через GitHub webhook

## Backup и восстановление

### База данных
```bash
# Backup (через Render CLI)
render postgres backup create sifibr-db

# Восстановление
render postgres backup restore sifibr-db backup_id
```

### Статические файлы
- Автоматически восстанавливаются при деплое
- Хранятся в WhiteNoise

## Production готовность

✅ **Безопасность**:
- DEBUG=False в production
- SECRET_KEY из переменных окружения
- HTTPS принудительно
- CORS настроен правильно

✅ **Производительность**:
- Gunicorn для production
- WhiteNoise для статических файлов
- PostgreSQL для данных
- Redis кеширование (при необходимости)

✅ **Мониторинг**:
- Health check endpoint
- Логирование настроено
- Error tracking готов

## Стоимость (Free Tier)

- **PostgreSQL**: Free (1GB, 1000 connections)
- **Web Service**: Free (750 hours/месяц)
- **Static Site**: Free (100GB bandwidth)

**Итого**: Полностью бесплатно для тестирования и небольших проектов!

## Дополнительные настройки

### Custom Domain
1. Render Dashboard → Static Site → Settings
2. Add Custom Domain: `collections.sifibr.ru`
3. Настройте DNS записи

### SSL Certificate
- Автоматически предоставляется Render
- Let's Encrypt сертификаты

### CDN
- Render автоматически использует CDN для статических файлов
- Глобальное распределение контента

---

**🎉 Поздравляем! Проект СИФИБР успешно развернут на Render.com**

Теперь байкальские микроорганизмы доступны всему миру! 🌊🦠 