# Развертывание СИФИБР на Render.com через Docker

Пошаговая инструкция по развертыванию проекта СИФИБР на Render.com с использованием Docker контейнера.

## Предварительные требования

- ✅ Аккаунт на [Render.com](https://render.com)
- ✅ Репозиторий проекта на GitHub
- ✅ Dockerfile готов для продакшн (включен в проект)

## Шаг 1: Создание базы данных PostgreSQL

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. Нажмите **"+ New"** → **"PostgreSQL"**
3. Заполните форму:
   - **Name**: `sifibr-collections-db`
   - **Database**: `sifibr_collections` (опционально)
   - **User**: `sifibr` (опционально)
   - **Region**: Выберите регион (запомните его!)
   - **PostgreSQL Version**: 15 (рекомендуется)
   - **Instance Type**: `Free` (для тестирования)
4. Нажмите **"Create Database"**

⚠️ **Важно**: Запомните выбранный регион - Web Service должен быть в том же регионе!

## Шаг 2: Получение DATABASE_URL

1. После создания БД откройте её страницу в Dashboard
2. Перейдите на вкладку **"Connect"**
3. Скопируйте **"Internal Database URL"** - он выглядит так:
   ```
   postgresql://sifibr:PASSWORD@HOST:5432/sifibr_collections
   ```

## Шаг 3: Создание Web Service

1. В Render Dashboard нажмите **"+ New"** → **"Web Service"**
2. Выберите **"Build and deploy from a Git repository"**
3. Подключите GitHub аккаунт (если не подключен)
4. Выберите репозиторий `site_collections_microorganisms`
5. Нажмите **"Connect"**

## Шаг 4: Настройка Web Service

### Основные настройки:

- **Name**: `sifibr-collections` (или любое уникальное имя)
- **Region**: 🔴 **Тот же, что и у БД!**
- **Branch**: `main`
- **Root Directory**: (оставить пустым)
- **Environment**: `Docker` 🔴 **Важно!**
- **Dockerfile Path**: `./Dockerfile`

### Дополнительные настройки:

- **Instance Type**: `Free` (для тестирования)
- **Auto-Deploy**: `Yes` (рекомендуется)

### Environment Variables (переменные окружения):

Добавьте следующие переменные:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | 🔴 **Вставьте Internal Database URL из шага 2** |
| `RENDER` | `true` |
| `DEBUG` | `False` |
| `SECRET_KEY` | (Render сгенерирует автоматически) |
| `ALLOWED_HOSTS` | `<your-service-name>.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://<your-service-name>.onrender.com` |

**Пример настройки переменных:**
```
DATABASE_URL = postgresql://sifibr:abc123...@internal-host:5432/sifibr_collections
RENDER = true
DEBUG = False
ALLOWED_HOSTS = sifibr-collections.onrender.com
CORS_ALLOWED_ORIGINS = https://sifibr-collections.onrender.com
```

## Шаг 5: Деплой

1. Нажмите **"Create Web Service"**
2. Render начнет автоматический деплой
3. Следите за логами в реальном времени

### Ожидаемые логи:

```
🚀 Starting SIFIBR Collections on Render...
✅ DATABASE_URL configured
📄 Running migrations...
📊 Creating test data...
👤 Creating superuser...
✅ Setup complete! Starting server on port 10000...
```

## Шаг 6: Проверка работы

### Health Check:
```bash
curl https://your-service-name.onrender.com/api/health/
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "database": "connected",
  "collections_count": 5,
  "strains_count": 7,
  "version": "1.0.0"
}
```

### API проверка:
```bash
curl https://your-service-name.onrender.com/api/collections/
```

### Админка Django:
```
https://your-service-name.onrender.com/admin/
Логин: admin
Пароль: sifibr_admin_2025
```

## Возможные проблемы и решения

### ❌ "could not translate host name 'db'"

**Причина**: Используется Docker-конфигурация вместо Render

**Решение**: 
1. Убедитесь, что `DATABASE_URL` настроен правильно
2. Проверьте, что переменная `RENDER=true` установлена
3. Убедитесь, что нет жестко прописанных хостов типа "db"

### ❌ "Connection refused" к базе данных

**Причина**: Web Service и БД в разных регионах

**Решение**: Оба сервиса должны быть в одном регионе Render

### ❌ "Static files not found"

**Причина**: Проблемы со сборкой статических файлов

**Решение**: Dockerfile уже содержит `collectstatic --noinput`

## Мониторинг и логи

### Просмотр логов:
1. В Render Dashboard откройте ваш Web Service
2. Перейдите на вкладку **"Logs"**
3. Фильтруйте по уровню: Error, Warning, Info

### Метрики:
- Использование CPU/RAM
- Время ответа API
- Количество запросов

### Уведомления:
Настройте уведомления на email или Slack при ошибках

## Масштабирование

### Бесплатный план ограничения:
- 750 часов в месяц
- 512MB RAM
- Засыпание при неактивности (15 минут)

### Обновление до платного плана:
1. Увеличенный лимит часов
2. Больше RAM/CPU
3. Без засыпания
4. SLA 99.9%

## Обновления

### Автоматические:
- Push в `main` ветку → автоматический деплой

### Ручные:
1. В Dashboard нажмите **"Manual Deploy"**
2. Выберите коммит или ветку

## Бэкапы

### База данных:
- Render автоматически создает бэкапы
- Доступны в разделе БД → **"Backups"**

### Файлы медиа:
- Используйте внешние хранилища (AWS S3, Cloudinary)
- Render не гарантирует сохранность файлов при рестарте

## Полезные ссылки

- 📋 [Render PostgreSQL Docs](https://render.com/docs/postgresql-creating-connecting)
- 🐳 [Render Docker Docs](https://render.com/docs/docker)
- 🔧 [Render Environment Variables](https://render.com/docs/environment-variables-secrets)
- 📊 [Render Health Checks](https://render.com/docs/health-checks)

---

**Создано для проекта СИФИБР СО РАН**  
*Сайт коллекций микроорганизмов Байкальского региона* 