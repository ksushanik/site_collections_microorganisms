from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
import os

def redirect_notice(request):
    """Показать информацию о переходе на React интерфейс"""
    # В production сразу редиректим на React
    if not settings.DEBUG or os.getenv('RENDER'):
        return redirect_to_react(request)
    return render(request, 'redirect_notice.html')

def redirect_to_react(request):
    """Прямое перенаправление на React приложение"""
    # Определяем URL React приложения в зависимости от окружения
    if os.getenv('RENDER'):
        # Production на Render
        react_url = 'https://sifibr-frontend.onrender.com/'
    else:
        # Local development  
        react_url = 'http://localhost:3000/'
    
    return HttpResponseRedirect(react_url) 