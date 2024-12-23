
import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

from main.models import Employee
def get_user(request):
    token = request.COOKIES.get('jwt')
    if token is None:
        raise AuthenticationFailed('Ты не аутетифицирован')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Токен истек')
    user = Employee.objects.filter(employeeId=payload['user']).first()
    if not user:
        raise AuthenticationFailed('Пользователь не найден')
    return user