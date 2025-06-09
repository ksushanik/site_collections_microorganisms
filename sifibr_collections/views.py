from django.http import JsonResponse
from django.template.response import TemplateResponse
from catalog.models import Strain, Collection

def api_info(request):
    """
    Информационная страница API backend.
    """
    # Базовая статистика
    total_strains = Strain.objects.count()
    total_collections = Collection.objects.count()
    
    if request.META.get('HTTP_ACCEPT', '').startswith('application/json'):
        # JSON ответ для API клиентов
        return JsonResponse({
            'service': 'СИФИБР СО РАН - API Backend',
            'version': '1.0.0',
            'description': 'REST API для коллекций микроорганизмов озера Байкал',
            'frontend_url': 'https://sifibr-frontend.onrender.com',
            'api_endpoints': {
                'health': '/api/health/',
                'strains': '/api/strains/',
                'collections': '/api/collections/',
                'admin': '/admin/'
            },
            'statistics': {
                'total_strains': total_strains,
                'total_collections': total_collections
            }
        })
    
    # HTML страница для браузеров
    context = {
        'total_strains': total_strains,
        'total_collections': total_collections,
        'frontend_url': 'https://sifibr-frontend.onrender.com',
        'title': 'СИФИБР СО РАН - API Backend'
    }
    
    return TemplateResponse(request, 'api_info.html', context) 