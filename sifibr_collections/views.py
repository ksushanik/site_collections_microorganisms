from django.shortcuts import render
from django.http import HttpResponseRedirect

def redirect_notice(request):
    """Показать информацию о переходе на React интерфейс"""
    return render(request, 'redirect_notice.html')

def redirect_to_react(request):
    """Прямое перенаправление на React приложение"""
    return HttpResponseRedirect('http://localhost:3001/') 