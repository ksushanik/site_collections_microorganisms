"""
URL configuration for sifibr_collections project.

СИФИБР СО РАН - Сайт коллекций микроорганизмов
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Каталог микроорганизмов
    path('', include('catalog.urls')),
    
    # Перенаправления для совместимости
    path('catalog/', RedirectView.as_view(url='/', permanent=True)),
]

# Обслуживание медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
