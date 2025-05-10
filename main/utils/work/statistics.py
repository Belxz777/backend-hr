
from datetime import datetime

import psutil
from rest_framework.decorators import api_view

from rest_framework.response import Response

from main.utils.recreatate.d import recreate_table
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
        'error_count': get_error_count(),
        'requests_per_minute': calculate_requests_per_minute(),
        'last_updated': datetime.now().isoformat()
    }
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

def get_error_count():
    """Get count of errors in last hour"""
    # Placeholder - implement actual error logging/counting
    return 0

def calculate_requests_per_minute():
    """Calculate average requests per minute"""
    # Placeholder - implement actual request tracking
    return 0
