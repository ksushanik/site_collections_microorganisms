#!/bin/bash

# Build script для Render.com

set -o errexit  # Остановить при ошибке

echo "🔧 Установка зависимостей Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput

echo "🗄️ Выполнение миграций..."
python manage.py migrate

echo "📊 Создание тестовых данных..."
python manage.py create_test_data

echo "✅ Сборка завершена!" 