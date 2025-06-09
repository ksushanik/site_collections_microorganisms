#!/bin/bash

# Entrypoint скрипт для Django backend
set -e

echo "🔬 Запуск СИФИБР Django Backend..."

# Функция для ожидания базы данных
wait_for_db() {
    echo "⏳ Ожидание подключения к PostgreSQL..."
    
    while ! nc -z $DB_HOST $DB_PORT; do
        echo "🔄 PostgreSQL недоступен - ожидание..."
        sleep 2
    done
    
    echo "✅ PostgreSQL доступен!"
}

# Функция для ожидания Redis
wait_for_redis() {
    echo "⏳ Ожидание подключения к Redis..."
    
    while ! nc -z $REDIS_HOST $REDIS_PORT; do
        echo "🔄 Redis недоступен - ожидание..."
        sleep 2
    done
    
    echo "✅ Redis доступен!"
}

# Извлекаем параметры подключения из DATABASE_URL
DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

# Извлекаем параметры Redis из REDIS_URL  
REDIS_HOST=$(echo $REDIS_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
REDIS_PORT=$(echo $REDIS_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

# Устанавливаем значения по умолчанию
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

# Ожидаем доступности сервисов
wait_for_db
wait_for_redis

echo "🔄 Выполнение миграций Django..."
python manage.py migrate --noinput

echo "📊 Создание суперпользователя (если не существует)..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sifibr.irk.ru', 'sifibr_admin_2025')
    print("✅ Суперпользователь создан: admin / sifibr_admin_2025")
else:
    print("ℹ️ Суперпользователь уже существует")
EOF

echo "🧬 Создание тестовых данных (если база пустая)..."
python manage.py shell << EOF
from catalog.models import Collection, Strain
if Collection.objects.count() == 0:
    exec(open('catalog/management/commands/create_extended_test_data.py').read())
    print("✅ Тестовые данные созданы")
else:
    print(f"ℹ️ База данных содержит {Collection.objects.count()} коллекций")
EOF

echo "📁 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "🎯 Проверка системы..."
python manage.py check --deploy

echo "✅ Инициализация завершена!"
echo "🚀 Запуск Django сервера..."

# Запускаем команду переданную в CMD
exec "$@" 