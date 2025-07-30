
import logging
import os
from dotenv import load_dotenv
import jwt
from rest_framework.exceptions import AuthenticationFailed

from main.models import Employee


logger = logging.getLogger('users')
load_dotenv()

coding_token = os.getenv('SECRET_KEY')
if not coding_token:
    raise RuntimeError("SECRET_KEY not configured in environment variables")

def get_user(request):
    token = request.COOKIES.get('jwt')
    if token is None:
        raise AuthenticationFailed('Не аутетифицирован')
    try:
        payload = jwt.decode(token, coding_token, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Токен истек')
    user = Employee.objects.filter(id=payload['user']).first()
    if not user:
        raise AuthenticationFailed('Пользователь не найден')
    return user