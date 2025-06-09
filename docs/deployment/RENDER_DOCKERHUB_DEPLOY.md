# Развертывание СИФИБР через Docker Hub на Render.com

Простой способ развертывания с использованием готового Docker образа.

## Преимущества подхода

✅ **Быстрый деплой** - образ уже собран  
✅ **Локальная сборка** - полный контроль процесса  
✅ **Кэширование** - Render не тратит время на сборку  
✅ **Переносимость** - один образ для разных платформ  
✅ **Стабильность** - избегаете проблем сборки на Render  

## Шаг 1: Подготовка Docker образа

### Локальная сборка и тестирование:

```bash
# Перейдите в корень проекта
cd site_collections_microorganisms

# Соберите образ
docker build -t sifibr/collections:latest .

# Протестируйте локально (опционально)
docker run --rm -p 8000:8000 \
  -e DATABASE_URL="sqlite:///test.db" \
  -e DEBUG=True \
  sifibr/collections:latest
```

### Публикация в Docker Hub:

```bash
# Войдите в Docker Hub
docker login

# Пометьте образ с версией
docker tag sifibr/collections:latest your-username/sifibr-collections:v1.0.0
docker tag sifibr/collections:latest your-username/sifibr-collections:latest

# Загрузите образы
docker push your-username/sifibr-collections:v1.0.0
docker push your-username/sifibr-collections:latest
```

**Альтернатива**: Используйте GitHub Actions для автоматической сборки

## Шаг 2: Настройка PostgreSQL на Render

1. Войдите в [Render Dashboard](https://dashboard.render.com)
2. **New** → **PostgreSQL**
3. Заполните форму:
   - **Name**: `sifibr-collections-db`
   - **Database**: `sifibr_collections`
   - **User**: `sifibr`
   - **Region**: Oregon (US West) - запомните!
   - **Instance Type**: Free
4. **Create Database**
5. Скопируйте **Internal Database URL** из раздела Connect

## Шаг 3: Создание Web Service из образа

1. **New** → **Web Service**
2. Выберите **"Deploy an existing image from a registry"**
3. Заполните форму:

### Основные настройки:
- **Image URL**: `your-username/sifibr-collections:latest`
- **Name**: `sifibr-collections`
- **Region**: Oregon (US West) ⚠️ **Тот же, что и БД!**
- **Instance Type**: Free

### Environment Variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://...` (из шага 2) |
| `RENDER` | `true` |
| `DEBUG` | `False` |
| `SECRET_KEY` | (автогенерация) |
| `ALLOWED_HOSTS` | `sifibr-collections.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://sifibr-collections.onrender.com` |
| `PORT` | `10000` |

4. **Create Web Service**

## Шаг 4: Проверка развертывания

### Health Check:
```bash
curl https://sifibr-collections.onrender.com/api/health/
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

### Административная панель:
- URL: https://sifibr-collections.onrender.com/admin/
- Логин: `admin`
- Пароль: `sifibr_admin_2025`

## Автоматизация через GitHub Actions

Создайте `.github/workflows/docker-publish.yml`:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: your-username/sifibr-collections

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: ${{ github.event_name != 'pull_request' }}
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## Обновление приложения

### Вариант 1: Автоматический (GitHub Actions)
```bash
git add .
git commit -m "feat: обновление функционала"
git push origin main
# GitHub Actions автоматически соберет и опубликует новый образ
# Render подтянет обновления при следующем деплое
```

### Вариант 2: Ручной
```bash
# Пересоберите образ
docker build -t your-username/sifibr-collections:v1.0.1 .
docker push your-username/sifibr-collections:v1.0.1

# В Render Dashboard:
# 1. Откройте ваш Web Service
# 2. Settings → Image URL → обновите тег
# 3. Manual Deploy
```

## Преимущества vs недостатки

### ✅ Преимущества:
- Быстрый деплой (1-2 минуты)
- Полный контроль сборки
- Локальное тестирование
- Кэширование слоев
- Возможность отката к предыдущим версиям
- Один образ для dev/staging/production

### ❌ Недостатки:
- Нужен Docker Hub аккаунт
- Дополнительный шаг (сборка и публикация)
- Размер образа влияет на скорость деплоя
- Нужно управлять тегами версий

## Сравнение методов

| Метод | Время деплоя | Контроль | Сложность |
|-------|-------------|----------|-----------|
| Git + Docker Build | 5-8 минут | Средний | Низкая |
| Docker Hub | 1-2 минуты | Высокий | Средняя |
| Blueprint | 10-15 минут | Низкий | Очень низкая |

## Рекомендации

**Используйте Docker Hub метод если:**
- Хотите максимальную скорость деплоя
- Нужен контроль над процессом сборки
- Планируете CI/CD pipeline
- Разворачиваете на нескольких платформах

**Используйте Git + Docker Build если:**
- Простота важнее скорости
- Не хотите настраивать дополнительные сервисы
- Команда небольшая

---

**Создано для проекта СИФИБР СО РАН**  
*Сайт коллекций микроорганизмов Байкальского региона* 