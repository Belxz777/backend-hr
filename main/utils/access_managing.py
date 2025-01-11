from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

import jwt,datetime

from ..models import Department, Employee
from ..serializer import EmployeeSerializer

def check_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Токен не предоставлен. ',
                         'possiblefix':'проверьте пожалуйста настройки запроса.Возможна ошибка чтения куки.'}, status=401)
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = Employee.objects.filter(employeeId=payload['user']).first()
       
        return True
           
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Токен истёк.'}, status=401)
    except jwt.InvalidTokenError:
        return Response({'error': 'Ошибка прочтения токена.',
                         'possiblefix':'Проверьте правильность токена.'}, status=401)


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
            raise AuthenticationFailed('Такого пользователя  пока не существует')
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
        isBoss = Department.objects.filter(headId=user.employeeId).first()
        if isBoss:
            response.data = {
                'message': 'Успешно вошли',
                'token': token,
                'isBoss': True,
                'departmentId': isBoss.departmentId
            }
            return response
        else:    
            response.data = {
            'message': 'Успешно вошли',
            'token': token,
            'isBoss': False
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
            return Response({'message': 'Токен еще не истек'}, status=200)
          else:
            new_payload = {'exp': datetime.datetime.now() + datetime.timedelta(days=10)}
            new_token = jwt.encode(new_payload, 'secret', algorithm='HS256')
            return Response({'message': 'Токен истек, но был обновлен', 'token': new_token.decode('utf-8')}, status=200)

        except jwt.exceptions.DecodeError:
            return Response({'message': 'Неверный токен ошибка декодировки.'}, status=400)
        
class Change_Password(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if token is None:
                raise AuthenticationFailed({'message': 'Ты не аутетифицирован '})
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Токен истек')
            user = Employee.objects.filter(employeeId=payload['user']).first()
            if not user:
                raise AuthenticationFailed('Пользователь не найден')
            new_password = request.data['new_password']
            old_password = request.data['old_password']
            if not new_password:
                raise AuthenticationFailed('Новый пароль не указан')
            if old_password != user.password:
                raise AuthenticationFailed('Неверный старый пароль')
            user.password = new_password
            user.save()
            return Response({'message': 'Пароль успешно изменен'})
        


class GetUser(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed({'message': 'Ты не аутетифицирован '})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')
        user = Employee.objects.filter(employeeId=payload['user']).values('firstName','lastName','jobid','departmentid').first()
        if not user:
            raise AuthenticationFailed('Пользователь не найден')
        return Response(user)