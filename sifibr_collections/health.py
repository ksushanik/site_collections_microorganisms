from django.http import JsonResponse
from django.db import connections
from catalog.models import Collection, Strain

def health_check(request):
    try:
        # Проверяем подключение к БД
        connections['default'].cursor()
        
        # Проверяем наличие данных
        collections_count = Collection.objects.count()
        strains_count = Strain.objects.count()
        
        return JsonResponse({
            'status': 'healthy', 
            'database': 'connected',
            'collections_count': collections_count,
            'strains_count': strains_count,
            'version': '1.0.0'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)
