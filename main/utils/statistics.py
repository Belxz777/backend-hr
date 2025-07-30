
from datetime import datetime

import psutil
from rest_framework.decorators import api_view

from rest_framework.response import Response
from main.log_handler import endpoint_handler

@api_view(['GET'])
def get_app_status_data(request):
    """
    Get statistics about application status
    Returns dict containing app status metrics
    """
    status_data = {
        'is_running': True,
        'uptime': get_system_uptime(),
        'memory_usage': get_memory_usage(),
        'cpu_usage': get_cpu_usage(),
        'active_connections': get_active_connections(),
        'last_updated': datetime.now().isoformat()
    }
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return Response(status_data)

def get_system_uptime():
    """Get system uptime in seconds"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.readline().split()[0])
        return uptime
    except FileNotFoundError:
        try:
            return psutil.boot_time()
        except:
            return 0
    except:
        return 0

def get_memory_usage():
    """Get current memory usage percentage"""
    try:
        return psutil.virtual_memory().percent
    except:
        return 0

def get_cpu_usage():
    """Get current CPU usage percentage"""
    try:
        return psutil.cpu_percent()
    except:
        return 0

def get_active_connections():
    """Get count of active connections"""
    try:
        connections = len(psutil.net_connections())
        return connections
    except:
        return 0
    
    
    # views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
import logging

from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from main.log_handler import endpoint_handler
logger = logging.getLogger('')
# class LogsAPIView(APIView):
#     def get(self, request):
#         level_filter = request.query_params.get('level', '').upper()
#         logs = list(endpoint_handler.logs)  # Копируем из deque
        
#         if level_filter in ['INFO', 'WARNING', 'CRITICAL']:
#             logs = [log for log in logs if log['level'] == level_filter]
        
#         # Форматируем timestamp
#         for log in logs:
#             log['timestamp'] = datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
#         return Response({
#             'count': len(logs),
#             'logs': logs[-100:]  # Последние 100 записей
#         })
# views.py
import os
from django.http import JsonResponse
from django.conf import settings

def get_logs(request):
    # Получаем параметры запроса
    level = request.GET.get('level', 'INFO').upper()
    limit = int(request.GET.get('limit', 100))
    
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level not in valid_levels:
        level = 'INFO'
    
    log_file_path = os.path.join(settings.BASE_DIR, 'django.log')
    logs = []
    
    try:
        # Читаем файл с конца, пока не соберем нужное количество записей
        with open(log_file_path, 'r') as f:
            # Используем оптимизированное чтение с конца файла
            for line in reverse_readline(f):
                if len(logs) >= limit:
                    break
                
                # Проверяем, содержит ли строка нужный уровень логирования
                if line.startswith(level + ' '):
                    logs.append({'message': line.strip()})
    
    except FileNotFoundError:
        pass
    
    # Разворачиваем список, так как читали с конца
    logs.reverse()
    
    return JsonResponse({
        'level': level,
        'logs': logs,
        'count': len(logs)
    })

def reverse_readline(file, buf_size=8192):
    """Генератор для чтения файла с конца (оптимизированное)"""
    file.seek(0, os.SEEK_END)
    pos = file.tell()
    buffer = ''
    
    while pos > 0 and len(buffer) < buf_size * 10:  # Ограничим максимальный буфер
        size = min(buf_size, pos)
        pos -= size
        file.seek(pos)
        
        chunk = file.read(size) + buffer
        lines = chunk.split('\n')
        
        # Оставляем неполную строку в буфере
        buffer = lines.pop(0)
        
        for line in reversed(lines):
            if line.strip():
                yield line
                
    if buffer.strip():
        yield buffer