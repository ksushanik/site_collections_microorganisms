# Развертывание СИФИБР как два сервиса на Render.com

Рекомендуемый подход: разделить фронт и бэк на два отдельных сервиса.

## Преимущества раздельного развертывания

✅ **Простота** - каждый сервис делает одну вещь хорошо  
✅ **Масштабируемость** - независимое масштабирование  
✅ **Скорость** - фронт обновляется мгновенно  
✅ **CDN** - автоматический CDN для статики  
✅ **Соответствие Render** - использует сильные стороны платформы  

## Шаг 1: Создание PostgreSQL базы данных

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. **New** → **PostgreSQL**
3. Настройки:
   - **Name**: `sifibr-collections-db`
   - **Database**: `sifibr_collections`
   - **User**: `sifibr`
   - **Region**: Oregon (US West)
   - **Instance Type**: Free
4. **Create Database**
5. Скопируйте **Internal Database URL**

## Шаг 2: Backend (Django API)

### Вариант A: Docker Hub образ
```bash
# Соберите и опубликуйте backend образ
./scripts/build-and-push.sh v1.0.0 gimmyhat backend
```

1. **New** → **Web Service**
2. **Deploy from registry**
3. **Image URL**: `gimmyhat/sifibr-collections:v1.0.0`
4. **Name**: `sifibr-backend`
5. **Region**: Oregon (US West) ⚠️ Тот же, что и БД

### Environment Variables:
| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Internal URL из БД) |
| `RENDER` | `true` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `sifibr-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://sifibr-frontend.onrender.com` |

### Вариант B: Git репозиторий
1. **New** → **Web Service**  
2. **Build from Git**
3. **Environment**: Docker
4. **Dockerfile Path**: `./Dockerfile`
5. Те же переменные окружения

## Шаг 3: Frontend (React Static Site)

1. **New** → **Static Site**
2. **Connect your repository**
3. **Name**: `sifibr-frontend`
4. **Region**: Oregon (US West)
5. **Build Command**: 
   ```bash
   cd frontend && npm ci && npm run build
   ```
6. **Publish Directory**: `frontend/dist`

### Environment Variables:
| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://sifibr-backend.onrender.com` |

## Шаг 4: Проверка развертывания

### Backend проверка:
```bash
curl https://sifibr-backend.onrender.com/api/health/
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

### Frontend проверка:
- Откройте: https://sifibr-frontend.onrender.com
- Должен загрузиться React интерфейс
- API запросы должны работать

### Полная система:
- 🌐 **Сайт**: https://sifibr-frontend.onrender.com
- 🔧 **API**: https://sifibr-backend.onrender.com/api/
- ⚙️ **Админка**: https://sifibr-backend.onrender.com/admin/

## Обновление приложения

### Backend обновление:
```bash
# Если используете Docker Hub
./scripts/build-and-push.sh v1.0.1 gimmyhat backend

# В Render Dashboard:
# 1. Откройте sifibr-backend
# 2. Settings → Image URL → обновите тег
# 3. Manual Deploy
```

### Frontend обновление:
```bash
git push origin main
# Static Site автоматически пересоберется
```

## Настройка CORS

В settings.py уже настроено:
```python
if not DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        "https://sifibr-frontend.onrender.com",
        "https://sifibr-backend.onrender.com",
    ])
```

## Мониторинг

### Логи Backend:
- Dashboard → sifibr-backend → Logs
- Ошибки Django, база данных, API

### Логи Frontend:
- Dashboard → sifibr-frontend → Logs  
- Сборка React, статические файлы

## Преимущества vs Недостатки

### ✅ Преимущества:
- Простая настройка и развертывание
- Автоматический CDN для фронта
- Независимое обновление сервисов
- Использует сильные стороны Render
- Быстрая загрузка статики
- Простое масштабирование

### ❌ Недостатки:
- Два отдельных URL (можно решить custom domain)
- Нужно настроить CORS
- Два сервиса = больше мониторинга

## Сравнение подходов

| Подход | Простота | Скорость | CDN | Масштабирование |
|--------|----------|----------|-----|-----------------|
| Два сервиса | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| Full-stack образ | ⭐⭐⭐ | ⭐⭐⭐ | ❌ | ⭐⭐⭐ |
| Blueprint | ⭐⭐⭐⭐ | ⭐⭐ | ✅ | ⭐⭐⭐⭐ |

## Рекомендации

**Используйте два сервиса если:**
- Хотите максимальную производительность фронта
- Планируете частые обновления UI
- Нужен автоматический CDN
- Команда работает отдельно над фронтом и бэком

**Используйте full-stack образ если:**
- Хотите один URL для всего приложения
- Простота развертывания важнее производительности
- Небольшая команда

---

**Создано для проекта СИФИБР СО РАН**  
*Сайт коллекций микроорганизмов Байкальского региона* 