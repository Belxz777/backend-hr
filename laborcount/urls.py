from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path('api/v1/',include('main.urls')),
    path('', lambda request: JsonResponse({'status': 'Server is running'})),
    
]