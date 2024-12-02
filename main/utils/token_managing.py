from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

import jwt,datetime

from ..models import Employee
from ..serializer import EmployeeSerializer
class RegisterView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    authentication_classes = []  # Disable authentication for login
    permission_classes = []      # Disable permissions for login
    
    def post(self, request):
        data = request.data
        login = data['login']
        password = data['password']
        user =Employee.objects.filter(login=login).first()
        if user is None:
            raise AuthenticationFailed('Нету такого пользователя')
        if not user.password == password:
            raise AuthenticationFailed('Неверный пароль')
        
        payload = {
            'user': user.employeeId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Успешно вошли',
            'token': token,
        }
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.set_cookie(key='jwt', value='', expires=0)
        response.data = {
            'message': 'Успешно вышли'
        }
        return response
    

class UserAuth(APIView):
    def get(self, request):

        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed({'message': 'Ты не аутетифицирован '})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')
        user = Employee.objects.filter(employeeId=payload['user']).first()
        serialize = EmployeeSerializer(user)
        return Response({'message': 'Ты аутетифицирован', 'token': token, 'userData': serialize.data})


class refresh_token(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        try:     
          payload = jwt.decode(token, "secret", algorithms=['HS256'])
          exp_time = datetime.datetime.fromtimestamp(payload['exp'])
          now = datetime.datetime.now()
          if now < exp_time:
            return Response({'message': 'Токен не истек'}, status=200)
          else:
            new_payload = {'exp': datetime.datetime.now() + datetime.timedelta(days=10)}
            new_token = jwt.encode(new_payload, 'secret', algorithm='HS256')
            return Response({'message': 'Токен истек, но был обновлен', 'token': new_token.decode('utf-8')}, status=200)

        except jwt.exceptions.DecodeError:
            return Response({'message': 'Неверный токен'}, status=400)