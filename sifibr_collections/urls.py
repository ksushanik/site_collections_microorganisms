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

urlpatterns = [
    # Админ панель Django
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('catalog.urls')),
    path('api/', include('search.urls')),
    path('api/', include('users.urls')),
    
    # Информационная страница о переходе на React (с кнопкой выбора)
    path('', views.redirect_notice, name='home'),
    
    # Прямое перенаправление для каталогов
    path('catalog/', views.redirect_to_react, name='catalog_redirect'),
    path('strains/', views.redirect_to_react, name='strains_redirect'),
    path('collections/', views.redirect_to_react, name='collections_redirect'),
    
    # Быстрое перенаправление
    path('react/', views.redirect_to_react, name='react_redirect'),
]

# Обслуживание медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
