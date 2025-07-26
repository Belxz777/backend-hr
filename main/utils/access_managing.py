from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.views import APIView
from dotenv import load_dotenv
import os
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q, F
import jwt
import datetime
from django.core.cache import cache
from rest_framework import status
from main.utils.auth import get_user
from ..models import Department, Deputy, Employee, Functions, Job
from ..serializer import AdminEmployeeSerializer, EmployeeSerializer
import logging
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('users')
load_dotenv()

coding_token = os.getenv('SECRET_KEY')
if not coding_token:
    raise RuntimeError("SECRET_KEY not configured in environment variables")

# Утилиты
def log_auth_attempt(user_id, success, ip=None):
    logger.info(
        f"Auth attempt - UserID: {user_id}, Success: {success}, IP: {ip}",
        extra={'user_id': user_id, 'auth_success': success, 'client_ip': ip}
    )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

class RegisterView(APIView):
    def post(self, request):
        try:
            login = request.data.get('login')
            if not login:
                return Response({'error': 'Логин не указан'}, status=status.HTTP_400_BAD_REQUEST)

            if Employee.objects.filter(login=login).exists():
                return Response({'error': 'Этот логин уже занят'}, status=status.HTTP_400_BAD_REQUEST)
            
            password = request.data.get('password')
            if not password or len(password) < 12:
                return Response(
                    {'error': 'Пароль должен содержать минимум 12 символов'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = EmployeeSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Registration error")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        try:
            login = request.data.get('login')
            password = request.data.get('password')
            
            if not login or not password:
                return Response(
                    {'error': 'Требуется логин и пароль'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = Employee.objects.filter(login=login).first()
            if not user:
                logger.warning(f"Login attempt for non-existent user: {login}")
                return Response(
                    {'error': 'Неверные учетные данные'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not check_password(password, user.password):
                log_auth_attempt(user.employeeId, False, get_client_ip(request))
                return Response(
                    {'error': 'Неверные учетные данные'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            payload = {
                'user': user.employeeId,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Срок жизни 1 день
                'iat': datetime.datetime.utcnow(),
                'position': user.position,
            }
            token = jwt.encode(payload, coding_token, algorithm='HS256')
            
            response = Response({
                'message': 'Вы успешно вошли в систему',
                'token': token,
                'time': datetime.datetime.now().strftime("%H:%M:%S")
            })
            response.set_cookie(
                key='jwt', 
                value=token, 
                httponly=True, 
                secure=True,  # Только для HTTPS
                samesite='Lax'
            )
            
            log_auth_attempt(user.employeeId, True, get_client_ip(request))
            return response

        except Exception as e:
            logger.exception("Login error")
            return Response(
                {'error': 'Внутренняя ошибка сервера'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserAuth(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Требуется аутентификация')

            payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            return Response({
                'message': 'Вы аутентифицированы', 
                'userData': payload
            })

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Неверный токен')
        except Exception as e:
            logger.exception("User auth error")
            raise AuthenticationFailed('Ошибка аутентификации')

@api_view(['GET'])
def user_list(request):
    try:
        current_user = get_user(request)
        if not current_user:
            raise AuthenticationFailed('Требуется аутентификация')

        if current_user.position < 4:
            raise PermissionDenied('Недостаточно прав')

        users = Employee.objects.all().values(
            'employeeId', 
            'firstName', 
            'lastName',
            'position'
        )
        return Response(users)

    except Exception as e:
        logger.exception("User list error")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def reset_password(request):
    try:
        admin_password = request.data.get('admin_password')
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')

        if not all([admin_password, user_id, new_password]):
            return Response(
                {'error': 'Необходимо указать все параметры'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if admin_password != os.getenv('RESET_PASSWORD_COMMAND'):
            return Response(
                {'error': 'Неверный пароль администратора'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = Employee.objects.get(employeeId=user_id)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        if len(new_password) < 12:
            return Response(
                {'error': 'Пароль должен содержать минимум 12 символов'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user.password = make_password(new_password)
        user.save()
        return Response({'message': 'Пароль успешно изменен'})

    except Exception as e:
        logger.exception("Password reset error")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
def check_token(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Токен не предоставлен. ',
                         'possiblefix':'проверьте пожалуйста настройки запроса.Возможна ошибка чтения куки.'}, status=401)
    try:
        payload = jwt.decode(token, coding_token, algorithms=['HS256'])
        user = Employee.objects.filter(employeeId=payload['user']).first()
       
        return True
           
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Токен истёк.'}, status=401)
    except jwt.InvalidTokenError:
        return Response({'error': 'Ошибка прочтения токена.',
                         'possiblefix':'Проверьте правильность токена.'}, status=401)


@api_view(['POST'])
def Reset_Password(request):
        try:
            admin_password = request.data.get('admin_password')
            user_id = request.data.get('user_id')
            new_password = request.data.get('new_password')
            
            ADMIN_PASSWORD = os.getenv('RESET_PASSWORD_COMMAND')
            if admin_password != ADMIN_PASSWORD:
                return Response({'message': 'Неверный пароль администратора'})
            try:
                userfound = Employee.objects.get(employeeId=user_id)
            except Employee.DoesNotExist:
                return Response({'message': 'Пользователь не найден'})
            
            hashed_password = make_password(new_password)
            userfound.password = hashed_password if new_password else userfound.password

            userfound.save()
        
            return Response({'message': 'Пароль пользователя успешно изменен'})
        
        except Exception as e:
            return Response({'message': 'Произошла ошибка при сбросе пароля', 'error': str(e)})

class refresh_token(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        try:     
          payload = jwt.decode(token, coding_token, algorithms=['HS256'])
          exp_time = datetime.datetime.fromtimestamp(payload['exp'])
          now = datetime.datetime.now()
          if now < exp_time:
            return Response({'message': 'Токен еще не истек'}, status=200)
          else:
            new_payload = {'exp': datetime.datetime.now() + datetime.timedelta(days=10)}
            new_token = jwt.encode(new_payload, coding_token, algorithm='HS256')
            return Response({'message': 'Токен истек, но был обновлен', 'token': new_token.decode('utf-8')}, status=200)

        except jwt.exceptions.DecodeError:
            return Response({'message': 'Неверный токен ошибка декодировки.'}, status=400)
class Change_Password(APIView):
        def post(self, request):
            token = request.COOKIES.get('jwt')
            if token is None:
                raise AuthenticationFailed({'message': 'Ты не аутетифицирован '})
            try:
                payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Токен истек')
            user = Employee.objects.filter(employeeId=payload['user']).first()
            if not user:
                raise AuthenticationFailed('Пользователь не найден')
            new_password = request.data['new_password']
            old_password = request.data['old_password']
            if not new_password:
                raise AuthenticationFailed('Новый пароль не указан')
            check_pass = check_password(old_password, user.password)
            if not check_pass:
                raise AuthenticationFailed({
                   'success': False,
                    'error': 'Неверный пароль',
                    'code': 'INVALID_CREDENTIALS',
                })
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Пароль успешно изменен'})


class GetUser(APIView):
    def get(self, request):
        # Проверка подключения к Redis
        try:
            cache.get('test_connection', 'test') 
        except Exception as e:
            logger.error(f"Ошибка подключения к кеш-системе: {str(e)}")
            # Не прерываем выполнение, продолжаем без кэша
        
        token = request.COOKIES.get('jwt')
        if not token:
            logger.warning('Пользователь не аутентифицирован')
            raise AuthenticationFailed({'message': 'Ты не аутентифицирован'})
        
        try:
            payload = jwt.decode(token, coding_token, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')
        
        # Формируем уникальный ключ кэша на основе user_id
        cache_key = f"user_data_{payload['user']}"
        
        # Пытаемся получить данные из кэша
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Данные пользователя {payload['user']} получены из кэша")
            return Response(cached_data, status=200)
        
        # Если данных нет в кэше, получаем их из БД
        user = Employee.objects.select_related('jobid', 'departmentid').filter(
            employeeId=payload['user']
        ).values(
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
        
        # Формируем базовую структуру ответа
        response_data = {
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
            }
        }

        if user['jobid__deputy'] is None:
            response_data['deputy'] = None
        else:
            deputies = Deputy.objects.filter(
                Q(deputyId=user['jobid__deputy']) | Q(compulsory=False)
            ).values('deputyId', 'deputyName', 'compulsory')
            response_data['deputy'] = list(deputies)
        
        try:
            cache.set(cache_key, response_data, timeout=500)
            logger.info(f"Данные пользователя {payload['user']} сохранены в кэш")
        except Exception as e:
            logger.error(f"Ошибка при сохранении в кэш: {str(e)}")
        
        return Response(response_data, status=200)
class Deposition(APIView):
    def patch(self,request):
            is_admin = get_user(request)
            if is_admin.position >= 4:
                new_pos = request.data['position']
                change = Employee.objects.filter(employeeId = request.data['empid']).update(position=new_pos)
                if change:
                    logger.info('Должность изменена, пользователь: {user}', is_admin.employeeId)
                    return Response({'message': 'Должность успешно изменена'})
                else:
                    logger.warning('Должность не изменена, пользователь: {user}', is_admin.employeeId)
                    return Response({'message': 'Должность не изменена'})
            else:
                logger.warning('Пользователь не аутетифицирован , попытка изменения должности id : {}'.format(is_admin.employeeId))
                return Response({'message': 'У вас нет доступа к этой странице'})
        
@api_view(['GET'])
def UserQuickView(request):
    try:
        # Получаем параметр поиска из query string
        search_query = request.GET.get('search', '').strip()
        only_mydepartment = request.GET.get('only_mydepartment', 'false').lower() == 'true'
        # Базовый запрос
        sender = get_user(request)
        if only_mydepartment and sender.position < 4:
            department_id = sender.departmentid.departmentId
            queryset = Employee.objects.filter(departmentid=department_id)  
        else:
            queryset = Employee.objects.all()
        
        
        # Применяем фильтр по фамилии, если есть поисковый запрос
        if search_query:
            queryset = queryset.filter(
                Q(lastName__icontains=search_query) | 
                Q(firstName__icontains=search_query)
            )
        
        # Получаем 15 случайных записей (или меньше, если их меньше 15)
        users = queryset.order_by('-position')[:15].values(
            'employeeId', 
            'firstName', 
            'lastName',
            'position',
          'position',
            job=F('jobid__jobName'),
    )
    
        return Response(list(users))
        
    except Exception as e:
        return Response(
            {'message': f'Произошла ошибка при получении данных: {str(e)}'},
            status=500
        )
        
api_view(['GET'])
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
    