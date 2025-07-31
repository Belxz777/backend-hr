from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import jwt
import logging

from main.models import Department
from main.serializer import DepartmentSerializer
from main.utils.auth import get_user

logger = logging.getLogger('departments')

class DepartmentManaging(APIView):
    def patch(self, request):
        """Обновление данных отдела"""
        logger.info(f"Department update request from {request.META.get('REMOTE_ADDR')}")
        try:
            department_id = request.query_params.get('id')
            if not department_id:
                return Response(
                    {'message': 'ID отдела обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            department = get_object_or_404(Department, id=department_id)
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response(
                    {
                        'message': 'Ошибки валидации',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            department = serializer.save()
            return Response(
                {
                    'message': 'Отдел успешно обновлен',
                    'data': DepartmentSerializer(department).data
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.exception(f"Department update error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """Удаление отдела"""
        logger.info(f"Department deletion request from {request.META.get('REMOTE_ADDR')}")
        try:
            user = get_user(request)
            if isinstance(user, Response):
                return user
                
            if user.position != 5:
                return Response(
                    {'message': 'Недостаточно прав для удаления отдела'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            department_id = request.query_params.get('id')
            if not department_id:
                return Response(
                    {'message': 'ID отдела обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            department = get_object_or_404(Department, id=department_id)
            department.delete()
            return Response(
                {'message': 'Отдел успешно удален'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.exception(f"Department deletion error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        logger.info(f"Department retrieval request from {request.META.get('REMOTE_ADDR')}")
        try:
            department_id = request.query_params.get('id')
        
            if department_id:
            # Получение конкретного отдела
                department = get_object_or_404(Department, id=department_id)
                return Response(
                {
                    'message': 'Данные отдела',
                    'data': DepartmentSerializer(department).data
                },
                status=status.HTTP_200_OK
            )
            else:
            # Получение списка всех отделов
                departments = Department.objects.all()
            
            # Опциональная фильтрация по правам пользователя
                # user = get_user(request)
                # if not isinstance(user, Response) and user.position < 4:
                #     departments = departments.filter(id=user.departmentid.id)
            
                serializer = DepartmentSerializer(departments, many=True)
                return Response(
                {
                    'message': 'Список отделов',
                    'data': serializer.data,
                    'count': departments.count()
                },
                status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.exception(f"Department retrieval error: {str(e)}")
            return Response(
            {'message': 'Внутренняя ошибка сервера'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DepartmentCreate(APIView):
    def post(self, request):
        """Создание нового отдела"""
        logger.info(f"Department creation request from {request.META.get('REMOTE_ADDR')}")
        try:
            user = get_user(request)
            if isinstance(user, Response):
                return user
                
            if user.position < 4:
                return Response(
                    {'message': 'Недостаточно прав для создания отдела'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = DepartmentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        'message': 'Ошибки валидации',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            department = serializer.save()
            return Response(
                {
                    'message': 'Отдел успешно создан',
                    'data': DepartmentSerializer(department).data
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.exception(f"Department creation error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
