from django.http import JsonResponse
from django.db import connections

def health_check(request):
    try:
        connections['default'].cursor()
        return JsonResponse({'status': 'healthy', 'database': 'ok'})
    except:
        return JsonResponse({'status': 'unhealthy'}, status=503)
