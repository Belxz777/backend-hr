from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from dotenv import load_dotenv
import os
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
import jwt
import datetime
from django.core.cache import cache
from rest_framework import status
from main.utils.auth import get_user
from ..models import Employee
from ..serializer import AdminEmployeeSerializer, EmployeeSerializer
import logging


logger = logging.getLogger(__name__)
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
"""
Стандарт если ошибка то status и message 
Пример :
Response({'message': 'Логин не указан'}, status=status.HTTP_400_BAD_REQUEST)
Статусные коды:
    200  успех
    
    201 успех создания
    
    401 для проблем аутентификации

    403 для недостатка прав

    404 для отсутствующих ресурсов

    400 для неверных параметров

    500 для серверных ошибок
"""
class RegisterView(APIView):
    def post(self, request):
        try:
            # Валидация обязательных полей
            required_fields = [ 'code', 'login', 'password', 'job_id', 'department_id']
            if not all(field in request.data for field in required_fields):
                return Response(
                    {'message': 'Необходимо указать все обязательные поля'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверка уникальности логина
            if Employee.objects.filter(code=request.data['code']).exists():
                return Response(
                    {'message': 'Этот код уже занят'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверка пароля
            if len(request.data['password']) < 12:
                return Response(
                    {'message': 'Пароль должен содержать минимум 12 символов'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Подготовка данных
            employee_data = request.data.copy()
            employee_data['password'] = make_password(employee_data['password'])
            
            serializer = EmployeeSerializer(data=employee_data)
            if not serializer.is_valid():
                return Response(
                    {
                        'message': 'Ошибки валидации данных',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(
                {
                    'message': 'Пользователь успешно зарегистрирован',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception(f"Registration error: {str(e)}")
            return Response(
                {'message': 'Произошла ошибка при регистрации'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []
    
#     def post(self, request):
#         try:
#             login = request.data.get('login')
#             password = request.data.get('password')
#             if not login or not password:
#                 return Response(
#                     {'message': 'Требуется логин и пароль '}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             user = Employee.objects.filter(login=login).first()
#             if not user:
#                 logger.warning(f"Login attempt for non-existent user: {login}")
#                 return Response(
#                     {'message': 'Указаны неверные данные учётной записи'}, 
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )
#             if not check_password(password, user.password):
#                 log_auth_attempt(user.id, False, get_client_ip(request))
#                 return Response(
#                     {'message': 'Указан неверный пароль'}, 
#                     status=status.HTTP_401_UNAUTHORIZED
#                 )
#             payload = {
#                 'user': user.id,
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),  # Срок жизни 14 дней
#                 'iat': datetime.datetime.utcnow(),
#                 'position': user.position,
#             }
#             token = jwt.encode(payload, coding_token, algorithm='HS256')
            
#             response = Response({
#                 'message': 'Вы успешно вошли в систему',
#                 'token': token,
#                 'time': datetime.datetime.now().strftime("%H:%M:%S")
#             },status=status.HTTP_200_OK)
#             response.set_cookie(
#                 key='jwt', 
#                 value=token, 
#                 httponly=True, 
#                 samesite='Lax'
#             ) 
#             log_auth_attempt(user.id, True, get_client_ip(request))
#             return response

#         except Exception as e:
#             logger.exception("Login error")
#             return Response(
#                 {'error': 'Внутренняя ошибка сервера, обратитесь в тех. поддержку '}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        try:
            code = request.data.get('code')
            password = request.data.get('password')
            if not code or not password:
                return Response(
                    {'message': 'Требуется логин и пароль '}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = Employee.objects.filter(code=code).first()
            if not user:
                logger.warning(f"Login attempt for non-existent user with code: {code}")
                return Response(
                    {'message': 'Указаны неверные данные учётной записи'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            if not check_password(password, user.password):
                log_auth_attempt(user.id, False, get_client_ip(request))
                return Response(
                    {'message': 'Указан неверный пароль'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            payload = {
                'user': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),  # Срок жизни 14 дней
                'iat': datetime.datetime.utcnow(),
                'position': user.position,
            }
            token = jwt.encode(payload, coding_token, algorithm='HS256')
            
            response = Response({
                'message': 'Вы успешно вошли в систему',
                'token': token,
                'time': datetime.datetime.now().strftime("%H:%M:%S")
            },status=status.HTTP_200_OK)
            response.set_cookie(
                key='jwt', 
                value=token, 
                httponly=True, 
                samesite='Lax'
            ) 
            log_auth_attempt(user.id, True, get_client_ip(request))
            return response

        except Exception as e:
            logger.exception("Login error")
            return Response(
                {'error': 'Внутренняя ошибка сервера, обратитесь в тех. поддержку '}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserAuth(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                raise Response({'message':"Требуется аутентификационный токен"},status=status.HTTP_403_FORBIDDEN)
            payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            return Response({
                'message': 'Вы аутентифицированы', 
                'userData': payload
            },status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError:
            return Response(
            {'message': 'Токен истек', 'code': 'token_expired'},
            status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response(
            {'message': 'Неверный токен', 'code': 'invalid_token'},
            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.exception(f"User auth error: {str(e)}")
            return Response(
                {
                'message': 'Ошибка аутентификации',
                'code': 'auth_error',
                'support': 'Обратитесь в техническую поддержку'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def user_list(request):
    try:
        current_user = get_user(request)
        if not current_user:
            return Response(
                {'message': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if current_user.position < 4:
            return Response(
                {'message': 'Недостаточно прав'},
                status=status.HTTP_403_FORBIDDEN
            )

        users = Employee.objects.all().values(
            'id', 
            'name', 
            'surname',
            'position'
        )
        return Response(
            {'message': 'Список пользователей', 'data': list(users)},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("User list error")
        return Response(
            {'message': 'Внутренняя ошибка сервера'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def reset_password(request):
    try:
        required_fields = ['admin_password', 'user_id', 'new_password']
        if not all(field in request.data for field in required_fields):
            return Response(
                {'message': 'Необходимо указать все параметры'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data['admin_password'] != os.getenv('RESET_PASSWORD_COMMAND'):
            return Response(
                {'message': 'Неверный пароль администратора'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = Employee.objects.get(id=request.data['user_id'])
        except Employee.DoesNotExist:
            return Response(
                {'message': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        if len(request.data['new_password']) < 12 and user.position<4:
            return Response(
                {'message': 'Пароль должен содержать минимум 12 символов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.password = make_password(request.data['new_password'])
        user.save()
        return Response(
            {'message': 'Пароль успешно изменен'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.exception("Password reset error")
        return Response(
            {'message': 'Внутренняя ошибка сервера'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class RefreshToken(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return Response(
                {'message': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:     
            payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            now = datetime.datetime.now()
            
            if now < exp_time:
                return Response(
                    {'message': 'Токен еще не истек'},
                    status=status.HTTP_200_OK
                )
            
            new_payload = {
                'user': payload['user'],
                'exp': datetime.datetime.now() + datetime.timedelta(days=14)
            }
            new_token = jwt.encode(new_payload, coding_token, algorithm='HS256')
            return Response(
                {
                    'message': 'Токен обновлен',
                    'token': new_token
                },
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {'message': 'Токен истек'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return Response(
                {'message': 'Неверный токен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception("Token refresh error")
            return Response(
                {'message': 'Ошибка обновления токена'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChangePassword(APIView):
    def post(self, request):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                return Response(
                    {'message': 'Требуется аутентификация'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try:
                payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response(
                    {'message': 'Токен истек'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            user = Employee.objects.filter(id=payload['user']).first()
            if not user:
                return Response(
                    {'message': 'Пользователь не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if 'new_password' not in request.data or not request.data['new_password']:
                return Response(
                    {'message': 'Новый пароль не указан'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if 'old_password' not in request.data:
                return Response(
                    {'message': 'Требуется текущий пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not check_password(request.data['old_password'], user.password):
                return Response(
                    {'message': 'Неверный текущий пароль'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.password = make_password(request.data['new_password'])
            user.save()
            return Response(
                {'message': 'Пароль успешно изменен'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.exception("Password change error")
            return Response(
                {'message': 'Ошибка изменения пароля'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetUser(APIView):
    def get(self, request):
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                logger.warning('Попытка доступа без аутентификации')
                return Response(
                    {'message': 'Требуется аутентификация','status':401},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            try:
                payload = jwt.decode(token, coding_token, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return Response(
                    {'message': 'Токен истек','status':401},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            except jwt.InvalidTokenError:
                return Response(
                    {'message': 'Неверный токен','status':400},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cache_key = f"user_data_{payload['user']}"
            try:
                cached_data = cache.get(cache_key)
                if cached_data:
                    logger.info(f"Данные пользователя {payload['user']} получены из кэша")
                    return Response(
                        {'message': 'Данные пользователя', 'data': cached_data,'status':200},
                        status=status.HTTP_200_OK
                    )
            except Exception as e:
                logger.error(f"Ошибка кэша: {str(e)}")
            
            user = Employee.objects.select_related('job', 'department').filter(
                id=payload['user']
            ).values(
                'id',
                'name',
                'code',
                'surname',
                'job',
                'department__name',
                'position',
                'job__name'
            ).first()
            
            if not user:
                return Response(
                    {'message': 'Пользователь не найден','status':404},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            response_data = {
                'user': {
                    'employeeId': user['id'],
                    'firstName': user['name'],
                    'code':user['code'],
                    'lastName': user['surname'],
                    'position': user['position']
                },
                'department': user['department__name'],
                'job': {
                    'jobName': user['job__name'],
                }
            }
            
            try:
                cache.set(cache_key, response_data, timeout=60*15)
                logger.info(f"Данные пользователя {payload['user']} сохранены в кэш")
            except Exception as e:
                logger.error(f"Ошибка сохранения в кэш: {str(e)}")
            
            return Response(
                {'message': 'Данные пользователя', 'data': response_data,'status':200},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.exception("Get user error")
            return Response(
                {'message': 'Ошибка получения данных пользователя','status':500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class Deposition(APIView):
    def patch(self, request):
        try:
            current_user = get_user(request)
            if not current_user:
                return Response(
                    {'message': 'Требуется аутентификация'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if current_user.position < 4:
                logger.warning(f'Попытка изменения должности без прав: {current_user.id}')
                return Response(
                    {'message': 'Недостаточно прав'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if 'id' not in request.data or 'position' not in request.data:
                return Response(
                    {'message': 'Необходимо указать ID пользователя и новую должность'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            updated = Employee.objects.filter(
                id=request.data['id']
            ).update(
                position=request.data['position']
            )
            
            if updated:
                logger.info(f'Должность изменена администратором: {current_user.id}')
                return Response(
                    {'message': 'Должность успешно изменена'},
                    status=status.HTTP_200_OK
                )
            else:
                logger.warning(f'Должность не изменена: {request.data["id"]}')
                return Response(
                    {'message': 'Пользователь не найден или данные не изменились'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.exception("Deposition change error")
            return Response(
                {'message': 'Ошибка изменения должности'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
def user_quick_view(request):
    try:
        # current_user = get_user(request)
        # if not current_user:
        #     return Response(
        #         {'message': 'Требуется аутентификация'},
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )
        
        search_query = request.GET.get('search', '').strip()
        only_mydepartment = request.GET.get('only_mydepartment', 'false').lower() == 'true'

        
        queryset = Employee.objects.all()
        
        if search_query:
            queryset = queryset.filter(
                Q(surname__icontains=search_query) | 
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query)  
            )
        
        users = queryset.order_by('-position')[:15].values(
            'id', 
            'name', 
            'code',
            'surname',
            'position',
            'job'
        )
        
        return Response(
            {'message': 'Список пользователей', 'data': list(users)},
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.exception("User quick view error")
        return Response(
            {'message': 'Ошибка получения списка пользователей'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def user_detail(request, pk):
    try:
        current_user = get_user(request)
        if not current_user:
            return Response(
                {'message': 'Требуется аутентификация'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if current_user.position < 4:
            return Response(
                {'message': 'Недостаточно прав'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user = Employee.objects.get(id=pk)
            serializer = AdminEmployeeSerializer(user)
            return Response(
                {'message': 'Данные пользователя', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except Employee.DoesNotExist:
            return Response(
                {'message': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Exception as e:
        logger.exception("User detail error")
        return Response(
            {'message': 'Ошибка получения данных пользователя'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )