
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from ...models import Department
from main.utils.auth import get_user
from django.core.cache import cache
from rest_framework.response import Response
@api_view(['GET'])
def departsdata(request):
        
    # Anti-DDoS protection
        request_ip = request.META.get('REMOTE_ADDR')
        request_key = f'request_count_{request_ip}'
        
        # Get current request count from cache

        request_count = cache.get(request_key, 0)
        
        # If request count exceeds limit, block the request
        if request_count >= 40:
            return Response({
                "message": "Too many requests. Please try again later.",
                "status": "blocked"
            }, status=429)
        
        # Increment request count and set expiry
        cache.set(request_key, request_count + 1, timeout=60)  # Reset after 60 seconds
        
        if request.method == 'GET':
            departments = Department.objects.all().values('departmentId', 'departmentName')
            if not departments:
                return Response(
                {
                    "message": "No departments found"
                }
            )
        return Response(
            departments
        )
