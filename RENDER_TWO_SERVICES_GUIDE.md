# 🚀 Полное руководство: Два сервиса СИФИБР на Render.com

## ✅ Готово к развертыванию!

### 📦 Подготовленные компоненты:
- **Backend**: Docker образ `gimmyhat/sifibr-collections:v1.0.0` опубликован ✅
- **Frontend**: Сборка успешна, готова к Static Site ✅

---

## 🎯 План развертывания (15 минут)

### 1️⃣ PostgreSQL База данных (2 минуты)
### 2️⃣ Backend Django API (5 минут)
### 3️⃣ Frontend React Static Site (5 минут)
### 4️⃣ Подключение и тестирование (3 минуты)

---

## Шаг 1: Создание PostgreSQL базы данных

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. **New** → **PostgreSQL**
3. Заполните форму:
   ```
   Name: sifibr-collections-db
   Database: sifibr_collections
   User: sifibr_user
   Region: Oregon (US West)
   PostgreSQL Version: 16
   Instance Type: Free
   ```
4. **Create Database**
5. 📋 **ВАЖНО**: Скопируйте **Internal Database URL** (начинается с `postgresql://`)

---

## Шаг 2: Backend (Django API)

### Создание Web Service

1. **New** → **Web Service**
2. **Deploy from registry**
3. Заполните:
   ```
   Image URL: gimmyhat/sifibr-collections:v1.0.0
   Name: sifibr-backend
   Region: Oregon (US West) ⚠️ Тот же, что и БД!
   Instance Type: Free
   ```

### Environment Variables

| Variable | Value | Описание |
|----------|-------|----------|
| `DATABASE_URL` | (Internal URL из БД) | Подключение к PostgreSQL |
| `RENDER` | `true` | Включает режим Render |
| `DEBUG` | `False` | Отключает отладку |
| `ALLOWED_HOSTS` | `sifibr-backend.onrender.com` | Разрешенные хосты |
| `CORS_ALLOWED_ORIGINS` | `https://sifibr-frontend.onrender.com` | CORS для фронта |

4. **Create Web Service**

### ⏱️ Ожидание развертывания (3-5 минут)

Render автоматически:
- Скачает Docker образ
- Выполнит миграции БД
- Создаст тестовые данные (5 коллекций, 7 штаммов)
- Создаст админа: `admin` / `sifibr_admin_2025`

### ✅ Проверка Backend

URL: `https://sifibr-backend.onrender.com/api/health/`

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

---

## Шаг 3: Frontend (React Static Site)

### Подготовка репозитория

⚠️ **Если изменили код**: Сначала запушьте изменения:
```bash
git add .
git commit -m "frontend: исправлена сборка для Render"
git push origin main
```

### Создание Static Site

1. **New** → **Static Site**
2. **Connect to Git repository** → выберите ваш репозиторий
3. Заполните:
   ```
   Name: sifibr-frontend
   Branch: main (или ваша основная ветка)
   Root Directory: (оставьте пустым)
   Build Command: cd frontend && npm ci && npm run build
   Publish Directory: frontend/dist
   ```

### Environment Variables для Frontend

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://sifibr-backend.onrender.com` |

4. **Create Static Site**

### ⏱️ Ожидание сборки (2-4 минуты)

Render выполнит:
```bash
cd frontend && npm ci && npm run build
```

### ✅ Проверка Frontend

URL: `https://sifibr-frontend.onrender.com`

Должно загрузиться:
- React приложение с синей темой Байкала
- Главная страница с информацией о СИФИБР
- Навигация: Каталог, Коллекции, О проекте

---

## Шаг 4: Подключение и тестирование

### Обновление CORS на Backend

1. Откройте **sifibr-backend** в Render Dashboard
2. **Environment** → измените:
   ```
   CORS_ALLOWED_ORIGINS = https://sifibr-frontend.onrender.com
   ```
3. **Manual Deploy** (если нужно)

### 🧪 Полное тестирование

**1. API тестирование:**
```bash
# Health check
curl https://sifibr-backend.onrender.com/api/health/

# Штаммы
curl https://sifibr-backend.onrender.com/api/strains/

# Коллекции  
curl https://sifibr-backend.onrender.com/api/collections/
```

**2. Frontend тестирование:**
- Откройте: https://sifibr-frontend.onrender.com
- **Каталог** → должна загрузиться таблица штаммов
- **Поиск** → попробуйте найти "Байкал" 
- **Фильтры** → выберите коллекцию

**3. Админка Django:**
- URL: https://sifibr-backend.onrender.com/admin/
- Логин: `admin` / `sifibr_admin_2025`
- Проверьте наличие данных

---

## 🎉 Результат: Полнофункциональная система

### 🌐 Ваши URL адреса:

| Сервис | URL | Назначение |
|--------|-----|------------|
| **Основной сайт** | https://sifibr-frontend.onrender.com | React интерфейс |
| **API** | https://sifibr-backend.onrender.com/api/ | REST API |
| **Админка** | https://sifibr-backend.onrender.com/admin/ | Управление данными |
| **Health Check** | https://sifibr-backend.onrender.com/api/health/ | Мониторинг |

### 📊 Данные:
- **5 научных коллекций** байкальских микроорганизмов
- **7 уникальных штаммов** с подробной информацией  
- **Географические данные** точек сбора
- **Таксономическая классификация**
- **Экстремофильные характеристики**

### 🔧 Функции:
- **Поиск и фильтрация** по всем характеристикам
- **Экспорт данных** в CSV и FASTA
- **Интерактивные карты** мест находок
- **Статистика и графики**
- **Адаптивный дизайн** для всех устройств

---

## 🛠️ Обновление системы

### Backend обновление:
```bash
# Соберите новую версию
./scripts/build-and-push.sh v1.0.1 gimmyhat backend

# В Render Dashboard:
# 1. sifibr-backend → Settings → Image URL  
# 2. Измените тег: v1.0.0 → v1.0.1
# 3. Manual Deploy
```

### Frontend обновление:
```bash
git add .
git commit -m "feat: обновление интерфейса"
git push origin main
# Static Site автоматически пересоберется
```

---

## 🔍 Мониторинг и логи

### Backend логи:
- Dashboard → **sifibr-backend** → **Logs**
- Django запросы, ошибки БД, API вызовы

### Frontend логи:
- Dashboard → **sifibr-frontend** → **Logs**
- Сборка React, статические файлы

### Мониторинг:
- Health Check API автоматически проверяет состояние
- Render автоматически перезапускает при сбоях
- Email уведомления о проблемах

---

## 🆘 Решение проблем

### Backend не запускается:
1. Проверьте `DATABASE_URL` в Environment Variables
2. Убедитесь, что регион Backend = регион БД
3. Проверьте логи на ошибки миграций

### Frontend не подключается к API:
1. Проверьте `VITE_API_URL` в Static Site
2. Обновите `CORS_ALLOWED_ORIGINS` на Backend
3. Проверьте, что Backend отвечает на Health Check

### CORS ошибки:
```bash
# Обновите CORS на Backend:
CORS_ALLOWED_ORIGINS=https://sifibr-frontend.onrender.com
```

---

## 📈 Масштабирование

### Paid планы Render:
- **Backend**: Faster instance + более workers
- **Frontend**: Faster builds + больше bandwidth
- **Database**: Больше connections + storage

### Производительность:
- Backend автоматически масштабируется
- Frontend на CDN - всегда быстрый
- Database оптимизирована для Django

---

## 🔐 Безопасность

### Настроено из коробки:
- ✅ HTTPS для всех сервисов
- ✅ Автоматические SSL сертификаты  
- ✅ CORS защита
- ✅ Django SECRET_KEY из переменных
- ✅ PostgreSQL с аутентификацией

### Рекомендации:
- Регулярно обновляйте зависимости
- Мониторьте логи на подозрительную активность
- Используйте strong passwords для админки

---

**🧬 Создано для СИФИБР СО РАН**  
*Сайт коллекций микроорганизмов Байкальского региона*

✨ **Успешно развернуто! Наслаждайтесь мощной платформой для научных исследований!** ✨ 