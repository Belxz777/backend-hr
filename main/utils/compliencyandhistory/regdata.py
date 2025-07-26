from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

import logging

from main.models import Department

logger = logging.getLogger(__name__)

@api_view(['GET'])
@cache_page(60 * 10)  # Кешируем весь ответ на 15 минут
def departsdata(request):
    # Anti-DDoS protection
    request_ip = request.META.get('REMOTE_ADDR')
    request_key = f'request_count_{request_ip}'
    
    # Получаем количество запросов из кеша
    request_count = cache.get(request_key, 0)
    
    if request_count >= 40:
        logger.warning(f"DDoS protection triggered for IP: {request_ip}")
        return Response({
            "message": "Too many requests. Please try again later.",
            "status": "blocked"
        }, status=429)
    
    # Увеличиваем счетчик запросов
    cache.set(request_key, request_count + 1, timeout=60)
    
    # Ключ для кеширования данных отделов
    cache_data_key = 'departments_data'
    
    # Пытаемся получить данные из кеша
    cached_departments = cache.get(cache_data_key)
    if cached_departments is not None:
        logger.info("Returning cached departments data")
        return Response(cached_departments)
    
    # Если данных нет в кеше, запрашиваем из БД
    departments = Department.objects.all().values('departmentId', 'departmentName')
    
    if not departments:
        logger.info("No departments found in database")
        return Response({"message": "No departments found"})
    
    # Конвертируем QuerySet в список для кеширования
    departments_list = list(departments)
    
    # Сохраняем в кеш на 1 час
    cache.set(cache_data_key, departments_list, timeout=60 * 10)
    
    return Response(departments_list)