#!/usr/bin/env python
"""
Альтернативная точка входа для СИФИБР Django приложения
Использует правильный WSGI модуль sifibr_collections.wsgi
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sifibr_collections.settings')
    
    try:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        print("✅ Django WSGI application ready")
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc 