    # your_app/views/health_views.py
from django.http import JsonResponse
from django.db import connection, DatabaseError
from django.core.cache import cache
import redis
import os
import platform
from datetime import datetime
import psutil  # pip install psutil (опционально)

def health_check(request):
    """
    Комплексная проверка состояния бэкенда
    """
    # Базовая информация
    info = {
        'status': 'success',
        'timestamp': datetime.now().isoformat(),
        'service': 'Django Backend',
        'version': '1.0.0'
    }
    
    # Проверка базы данных
    db_status = check_database()
    info['database'] = db_status
    
    # Проверка кэша
    cache_status = check_cache()
    info['cache'] = cache_status
    
    # Системная информация
    system_info = get_system_info()
    info['system'] = system_info
    
    # Проверка моделей (опционально)
    models_status = check_models()
    info['models'] = models_status
    
    # Общий статус
    if db_status['status'] == 'error' or cache_status['status'] == 'error':
        info['status'] = 'degraded'
    if db_status['status'] == 'error' and cache_status['status'] == 'error':
        info['status'] = 'error'
    
    # HTTP статус код
    status_code = 200
    if info['status'] == 'error':
        status_code = 503  # Service Unavailable
    elif info['status'] == 'degraded':
        status_code = 206  # Partial Content
    
    return JsonResponse(info, status=status_code)

def check_database():
    """Проверка подключения к базе данных"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        # Получаем информацию о БД
        db_info = {
            'status': 'connected',
            'engine': connection.vendor,
            'version': get_database_version(),
            'tables_count': get_tables_count(),
            'test_query': 'success'
        }
        
        # Проверяем основные таблицы
        try:
            from django.contrib.auth.models import User
            user_count = User.objects.count() if 'auth_user' in connection.introspection.table_names() else 0
            db_info['user_count'] = user_count
        except:
            db_info['user_count'] = 'unknown'
            
    except DatabaseError as e:
        db_info = {
            'status': 'error',
            'error': str(e),
            'engine': connection.vendor if hasattr(connection, 'vendor') else 'unknown'
        }
    except Exception as e:
        db_info = {
            'status': 'error',
            'error': f'Unexpected error: {str(e)}'
        }
    
    return db_info

def check_cache():
    """Проверка работы кэша"""
    try:
        # Тестируем кэш
        test_key = 'health_check_test'
        test_value = 'test_data'
        
        # Записываем
        cache.set(test_key, test_value, 30)
        
        # Читаем
        retrieved_value = cache.get(test_key)
        
        cache_info = {
            'status': 'connected' if retrieved_value == test_value else 'degraded',
            'backend': get_cache_backend_name(),
            'test': 'success' if retrieved_value == test_value else 'failed'
        }
        
        # Дополнительная информация для Redis
        if hasattr(cache, 'client'):
            try:
                cache_info['ping'] = cache.client.get_client().ping()
            except:
                cache_info['ping'] = False
                
    except Exception as e:
        cache_info = {
            'status': 'error',
            'error': str(e),
            'backend': get_cache_backend_name()
        }
    
    return cache_info

def get_system_info():
    """Получение системной информации"""
    try:
        system_info = {
            'python_version': platform.python_version(),
            'django_version': get_django_version(),
            'platform': platform.system(),
            'hostname': platform.node(),
            'uptime': get_uptime(),
        }
        
        # Добавляем информацию о памяти (если установлен psutil)
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            system_info['memory_usage_mb'] = round(memory_info.rss / 1024 / 1024, 2)
            system_info['cpu_percent'] = process.cpu_percent()
        except ImportError:
            system_info['psutil'] = 'not_available'
            
    except Exception as e:
        system_info = {
            'error': f'Failed to get system info: {str(e)}'
        }
    
    return system_info

def check_models():
    """Проверка основных моделей приложения"""
    try:
        from models import Department, Job, Employee  # Замените на ваше приложение
        
        models_info = {
            'departments_count': Department.objects.count(),
            'jobs_count': Job.objects.count(),
            'employees_count': Employee.objects.count(),
            'status': 'success'
        }
    except Exception as e:
        models_info = {
            'status': 'error',
            'error': str(e)
        }
    
    return models_info

# Вспомогательные функции
def get_database_version():
    """Получение версии базы данных"""
    try:
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("SELECT version()")
                version = cursor.fetchone()[0]
            elif connection.vendor == 'mysql':
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
            else:
                version = 'unknown'
        return version.split()[0] if version else 'unknown'
    except:
        return 'unknown'

def get_tables_count():
    """Получение количества таблиц в БД"""
    try:
        return len(connection.introspection.table_names())
    except:
        return 'unknown'

def get_cache_backend_name():
    """Получение названия бэкенда кэша"""
    try:
        return cache.__class__.__name__
    except:
        return 'unknown'

def get_django_version():
    """Получение версии Django"""
    import django
    return django.get_version()

def get_uptime():
    """Получение времени работы системы"""
    try:
        return int(psutil.boot_time()) if psutil else 'unknown'
    except:
        return 'unknown'