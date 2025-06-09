# Dockerfile для Render.com deployment
FROM python:3.11-slim

# Метаданные
LABEL maintainer="SIFIBR SB RAS <sifibr@sifibr.irk.ru>"
LABEL description="SIFIBR Microorganisms Collections - Render Deployment"

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Устанавливаем системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        gettext \
        postgresql-client \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Копируем код приложения
COPY . .

# Создаем необходимые директории
RUN mkdir -p /app/staticfiles /app/media

# Собираем статические файлы
RUN python manage.py collectstatic --noinput --clear

# Создаем entrypoint скрипт для Render
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🚀 Starting SIFIBR Collections on Render..."\n\
\n\
# Выполняем миграции\n\
echo "📄 Running migrations..."\n\
python manage.py migrate --noinput\n\
\n\
# Создаем тестовые данные\n\
echo "📊 Creating test data..."\n\
python manage.py create_test_data || echo "Test data already exists"\n\
\n\
# Создаем суперпользователя\n\
echo "👤 Creating superuser..."\n\
python manage.py shell -c "\
from django.contrib.auth.models import User;\
User.objects.filter(username=\"admin\").exists() or \
User.objects.create_superuser(\"admin\", \"admin@sifibr.irk.ru\", \"sifibr_admin_2025\")\
" || echo "Admin user already exists"\n\
\n\
echo "✅ Setup complete! Starting server on port $PORT..."\n\
\n\
# Запускаем сервер с динамическим портом от Render\n\
exec gunicorn sifibr_collections.wsgi:application \\\n\
    --bind 0.0.0.0:$PORT \\\n\
    --workers 4 \\\n\
    --worker-class sync \\\n\
    --timeout 120 \\\n\
    --keep-alive 2 \\\n\
    --access-logfile - \\\n\
    --error-logfile -\n\
' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/health/ || exit 1

# Expose динамический порт
EXPOSE $PORT

ENTRYPOINT ["/entrypoint.sh"] 