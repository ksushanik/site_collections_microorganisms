#!/bin/bash

# Скрипт сборки и публикации Docker образа СИФИБР на Docker Hub
# Использование: ./scripts/build-and-push.sh [version] [username] [type]
# type: backend (только Django) | fullstack (Django + React)

set -e

# Параметры по умолчанию
DEFAULT_USERNAME="gimmyhat"
DEFAULT_VERSION="latest"
DEFAULT_TYPE="fullstack"

# Получаем параметры
USERNAME=${2:-$DEFAULT_USERNAME}
VERSION=${1:-$DEFAULT_VERSION}
BUILD_TYPE=${3:-$DEFAULT_TYPE}

if [ "$BUILD_TYPE" = "fullstack" ]; then
    IMAGE_NAME="$USERNAME/sifibr-collections-fullstack"
    DOCKERFILE="Dockerfile.fullstack"
else
    IMAGE_NAME="$USERNAME/sifibr-collections"
    DOCKERFILE="Dockerfile"
fi

echo "🐳 Сборка и публикация Docker образа СИФИБР"
echo "======================================"
echo "👤 Docker Hub username: $USERNAME"
echo "🏷️  Версия: $VERSION"
echo "🔧 Тип сборки: $BUILD_TYPE"
echo "📦 Образ: $IMAGE_NAME:$VERSION"
echo "📄 Dockerfile: $DOCKERFILE"
echo ""

# Проверяем, что находимся в корне проекта
if [ ! -f "manage.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из корня проекта"
    exit 1
fi

# Проверяем Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Ошибка: Docker не установлен"
    exit 1
fi

# Собираем образ
echo "🔨 Сборка образа..."
docker build -f "$DOCKERFILE" -t "$IMAGE_NAME:$VERSION" .

# Если не latest, также помечаем как latest
if [ "$VERSION" != "latest" ]; then
    echo "🏷️  Создание тега latest..."
    docker tag "$IMAGE_NAME:$VERSION" "$IMAGE_NAME:latest"
fi

# Проверяем авторизацию в Docker Hub
echo "🔑 Проверка авторизации Docker Hub..."
if ! docker info | grep -q "Username:"; then
    echo "❗ Требуется авторизация в Docker Hub"
    echo "Выполните: docker login"
    read -p "Войти сейчас? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker login
    else
        echo "❌ Отменено"
        exit 1
    fi
fi

# Тестируем образ (опционально)
echo "🧪 Быстрый тест образа..."
CONTAINER_ID=$(docker run -d --rm -e DEBUG=True -e DATABASE_URL="sqlite:///test.db" "$IMAGE_NAME:$VERSION")
sleep 5

# Проверяем, что контейнер запустился
if docker ps | grep -q "$CONTAINER_ID"; then
    echo "✅ Образ работает корректно"
    docker stop "$CONTAINER_ID" > /dev/null 2>&1 || true
else
    echo "❌ Ошибка: Образ не запускается"
    exit 1
fi

# Публикуем образ
echo "📤 Публикация в Docker Hub..."
docker push "$IMAGE_NAME:$VERSION"

if [ "$VERSION" != "latest" ]; then
    docker push "$IMAGE_NAME:latest"
fi

echo ""
echo "🎉 Готово!"
echo "======================================"
echo "📦 Опубликованный образ: $IMAGE_NAME:$VERSION"
echo "🌐 Docker Hub: https://hub.docker.com/r/$USERNAME/sifibr-collections"
echo ""
echo "🚀 Для деплоя на Render.com:"
echo "   1. New → Web Service → Deploy from registry"
echo "   2. Image URL: $IMAGE_NAME:$VERSION"
echo "   3. Добавьте переменные окружения (см. документацию)"
echo ""
echo "📚 Полная инструкция: docs/deployment/RENDER_DOCKERHUB_DEPLOY.md" 