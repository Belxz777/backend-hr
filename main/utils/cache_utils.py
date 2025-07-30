from django.core.cache import cache
from django.db import models
from functools import wraps
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def model_cache_key(model_instance: models.Model):
    """
    Генерирует ключ кеша для экземпляра модели
    """
    return f"{model_instance._meta.model_name}:{model_instance.pk}"

def invalidate_model_cache(model_class: models.Model):
    """
    Декоратор для инвалидации кеша модели после изменении модели
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            
            # Получаем ID из запроса или ответа
            instance_id = kwargs.get('id') or request.data.get('id') or (response.data.get('id') if hasattr(response, 'data') else None)
            
            if instance_id:
                cache_key = f"{model_class._meta.model_name}:{instance_id}"
                cache.delete(cache_key)
                logger.info(f"Cache invalidated for {cache_key}")
            return response
        return wrapped_view
    return decorator

def cache_model(timeout=None):
    """
    Декоратор для кеширования представлений, возвращающих данные модели
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            cache_key = None
            model_name = view_func.__name__.lower()
            
            # Для детальных представлений (с ID)
            if 'id' in kwargs:
                cache_key = f"{model_name}:{kwargs['id']}"
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    logger.info(f"Cache hit for {cache_key}")
                    return Response(cached_data)
            
            # Для списковых представлений
            else:
                params = request.GET.urlencode()
                cache_key = f"{model_name}_list:{params}"
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    logger.info(f"Cache hit for {cache_key}")
                    return Response(cached_data)
            
            response = view_func(request, *args, **kwargs)
            
            if response.status_code == 200 and cache_key:
                cache.set(cache_key, response.data, timeout=timeout)
                logger.info(f"Cache set for {cache_key}")
            
            return response
        return wrapped_view
    return decorator