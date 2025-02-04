
import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache

from main.models import Employee
def get_user(request):
    token = request.COOKIES.get('jwt')
    if token is None:
        print("dfsfsdfsdf")
        raise AuthenticationFailed('Ты не аутетифицирован')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Токен истек')
    cached_user = cache.get(f'user_{payload["user"]}')
    if cached_user:
        return cached_user
    user = Employee.objects.filter(employeeId=payload['user']).first()
    cache.set(f'user_{payload["user"]}', user, timeout=120)
    if not user:
        raise AuthenticationFailed('Пользователь не найден')
    return user