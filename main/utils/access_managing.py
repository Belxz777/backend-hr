from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
import jwt,datetime
from django.core.cache import cache
from rest_framework import status
from main.utils.auth import get_user
from ..models import Department, Deputy, Employee, Functions, Job
from ..serializer import AdminEmployeeSerializer, EmployeeSerializer

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
        # Check if login already exists
        if Employee.objects.filter(login=request.data.get('login')).exists():
            return Response({'error': 'Этот логин уже занят'}, status=400)
        
        if serializer.is_valid():
            password = make_password(request.data.get('password'))
            serializer.validated_data['password'] = password
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
class LoginView(APIView):
    authentication_classes = []  # Disable authentication for login
    permission_classes = []      # Disable permissions for login
    
    def post(self, request):
        data = request.data
        login = request.data.get('login')
        password = request.data.get('password')
        
        # Валидация входных данных
        if not login or not password:
            return Response(
                {
                    'success': False,
                    'error': 'Требуется логин и пароль',
                    'code': 'MISSING_CREDENTIALS'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = Employee.objects.filter(login=login).first()
        if user is None:
            raise AuthenticationFailed('Такого пользователя  пока не существует')
        
        check_pass = check_password(data['password'], user.password)
        if not check_pass:
            raise AuthenticationFailed('Неверный пароль')
        print(check_pass)
        payload = {
            'user': user.employeeId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10),
            'iat': datetime.datetime.utcnow(),
            'position': user.position,
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'Успешно вошли',
            'token': token,
            'time':  datetime.datetime.now().strftime("%H:%M:%S")
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
        # user = Employee.objects.filter(employeeId=payload['user']).first()
        # serialize = EmployeeSerializer(user)
        return Response({'message': 'Ты аутетифицирован', 'userData': payload})


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
        
class PasswordRecovery(APIView):
    def post(self, request):
        passf = request.data['new_password']
        emp_id = request.data['employeeId']
        if not passf:
            raise AuthenticationFailed('Не указан email')       
        user = Employee.objects.filter(employeeId=emp_id).first()
        if not user:
            raise AuthenticationFailed('Пользователь не найден')
        
        user.password = passf
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
        user = Employee.objects.select_related('jobid', 'departmentid').filter(employeeId=payload['user']).values(
            'employeeId',
            'firstName',
            'lastName',
            'jobid',
            'departmentid__departmentName',
            'position',
            'jobid__jobName',
            'jobid__deputy'
        ).first()   
        
        if not user:
            raise AuthenticationFailed('Пользователь не найден')
        
        if user['jobid__deputy'] is None:
            deputy = None
            return Response({
                'user': {
                    'employeeId': user['employeeId'],
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'position': user['position']
                },
                'department': user['departmentid___departmentName'],
                'job': {
                    'jobName': user['jobid__jobName'],
                    'deputy': user['jobid__deputy']
                },
                'deputy': deputy,
            },status=200)
        else:
            deputies = Deputy.objects.filter(Q(deputyId=user['jobid__deputy']) | Q(compulsory=False)).values('deputyId', 'deputyName', 'compulsory')
            return Response({
                'user': {
                    'employeeId': user['employeeId'],
                    'firstName': user['firstName'],
                    'lastName': user['lastName'],
                    'position': user['position']
                },
                'department': user['departmentid__departmentName'],
                'job': {
                    'jobName': user['jobid__jobName'],
                    'deputy': user['jobid__deputy']
                },
                'deputy': list(deputies),
            },status=200)
class Deposition(APIView):
    def patch(self,request):
            new_pos = request.data['position']
            print(new_pos)
            change = Employee.objects.filter(employeeId = request.data['empid']).update(position=new_pos)
            print(change)
            return Response({'message': 'Должность успешно изменена'})
        
@api_view(['GET'])
def UserList(request):
    user = get_user(request)
    if user:
        if user.position >=4:
            users = Employee.objects.all()
            return Response(users.values('employeeId', 'firstName', 'lastName','position'))
        else:
            return Response({'message': 'У вас нет доступа к этой странице'})
    else:
        return Response({'message': 'Ты не аутетифицирован '})
    

@api_view(['GET'])
def UserDetail(request, pk):
    user = get_user(request)
    if user:
        if user.position >= 4:
            try:
                userfound = Employee.objects.get(employeeId=pk)
                serializer = AdminEmployeeSerializer(userfound)
                return Response(serializer.data)
            except Employee.DoesNotExist:
                return Response({'message': 'Пользователь не найден'})
        else:
            return Response({'message': 'У вас нет доступа к этой странице'})
    else:
        return Response({'message': 'Ты не аутетифицирован '})