"""
URL configuration for sifibr_collections project.

СИФИБР СО РАН - Сайт коллекций микроорганизмов
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views
from .health import health_check

urlpatterns = [
    # Админ панель Django
    path('admin/', admin.site.urls),
    
    # Health check for monitoring
    path('api/health/', health_check, name='health_check'),
    
    # API endpoints
    path('api/', include('catalog.urls')),
    path('api/', include('search.urls')),
    path('api/', include('users.urls')),
    
    # API-only backend, главная страница отдает информацию о API
    path('', views.api_info, name='api_info'),
]

# Обслуживание статических файлов (всегда)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
