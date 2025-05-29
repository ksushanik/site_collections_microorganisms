from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'catalog'

# API маршруты для REST
router = DefaultRouter()
router.register(r'collections', views.CollectionViewSet)
router.register(r'strains', views.StrainViewSet)
router.register(r'genome-sequences', views.GenomeSequenceViewSet)
router.register(r'publications', views.PublicationViewSet)

urlpatterns = [
    # API endpoints - только для React приложения
    path('', include(router.urls)),
    path('search/', views.AdvancedSearchAPIView.as_view(), name='api_search'),
    path('stats/', views.StatisticsAPIView.as_view(), name='api_stats'),  
    path('export/<str:format>/', views.ExportAPIView.as_view(), name='api_export'),
] 