"""
URL configuration for sifibr_collections project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponse

def home(request):
    return HttpResponse("""
    <h1>🧬 СИФИБР: Коллекции микроорганизмов</h1>
    <p>Добро пожаловать на сайт коллекций микроорганизмов Сибирского института физиологии и биохимии растений СО РАН!</p>
    <p>Статус: <strong>Развертывание успешно!</strong> ✅</p>
    <ul>
        <li><a href="/admin/">Администрирование</a></li>
        <li><a href="/api/v1/">API</a></li>
    </ul>
    <p><em>Байкальские экстремофилы - уникальные организмы озера Байкал</em></p>
    """)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('catalog.urls')),
    
    # API endpoints
    path('api/', include('search.urls')),
    path('api/', include('users.urls')),
    
    # Информационная страница о переходе на React (с кнопкой выбора)
    path('catalog/', RedirectView.as_view(url='/react/'), name='catalog_redirect'),
    path('strains/', RedirectView.as_view(url='/react/'), name='strains_redirect'),
    path('collections/', RedirectView.as_view(url='/react/'), name='collections_redirect'),
    
    # Быстрое перенаправление
    path('react/', RedirectView.as_view(url='/react/'), name='react_redirect'),
]

# Обслуживание медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
