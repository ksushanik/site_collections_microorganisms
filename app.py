"""
WSGI файл для совместимости с Render.com
Render по умолчанию ищет app:app, поэтому создаем правильный импорт
"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifibr_collections.settings')

# Импорт Django WSGI приложения
from django.core.wsgi import get_wsgi_application

# Создаем приложение, которое ожидает Render (app)
app = get_wsgi_application() 