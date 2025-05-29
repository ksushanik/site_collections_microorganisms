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
    # Веб-интерфейс
    path('', views.CatalogHomeView.as_view(), name='home'),
    
    # Коллекции
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collections/<uuid:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    
    # Штаммы
    path('strains/', views.StrainListView.as_view(), name='strain_list'),
    path('strains/<uuid:pk>/', views.StrainDetailView.as_view(), name='strain_detail'),
    path('strains/search/', views.StrainSearchView.as_view(), name='strain_search'),
    
    # Специальные страницы
    path('baikal-extremophiles/', views.BaikalExtremophilesView.as_view(), name='baikal_extremophiles'),
    path('biotechnology/', views.BiotechnologyView.as_view(), name='biotechnology'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/search/', views.AdvancedSearchAPIView.as_view(), name='api_search'),
    path('api/stats/', views.StatisticsAPIView.as_view(), name='api_stats'),
    path('api/export/<str:format>/', views.ExportAPIView.as_view(), name='api_export'),
] 