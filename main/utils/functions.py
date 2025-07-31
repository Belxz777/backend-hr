from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

import logging

from main.models import Functions
from main.serializer import FunctionsSerializer
from main.utils.auth import get_user

logger = logging.getLogger('functions')
class FunctionsManage(APIView):
    def check_permissions(self, request):
        """Проверка прав доступа (токен и позиция >4)"""
        user = get_user(request)
        if isinstance(user, Response):
            return user
        if user.position <= 4:
            return Response(
                {'message': 'Недостаточно прав для выполнения операции'},
                status=status.HTTP_403_FORBIDDEN
            )
        return None

    def get_id_from_request(self, request):
        """Получаем ID из query параметров или URL"""
        # Для GET/DELETE/PATCH с ?id= в query params
        id_from_query = request.query_params.get('id')
        if id_from_query:
            return id_from_query
        
        # Для URL типа /functions/<id>/
        return self.kwargs.get('id')

    def get(self, request):
        """Получение списка функций или конкретной функции"""
        try:
            # Проверка прав
            # permission_check = self.check_permissions(request)
            # if permission_check:
            #     return permission_check

            function_id = self.get_id_from_request(request)
            if function_id:
                function = get_object_or_404(Functions, id=function_id)
                serializer = FunctionsSerializer(function)
                return Response(
                    {'message': 'Функция получена', 'data': serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                functions = Functions.objects.all()
                serializer = FunctionsSerializer(functions, many=True)
                return Response(
                    {'message': 'Список функций', 'data': serializer.data},
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            logger.exception(f"Functions get error: {str(e)}")
            return Response(
                {'message': 'Ошибка получения данных'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Создание новой функции"""
        try:
            # Проверка прав
            permission_check = self.check_permissions(request)
            if permission_check:
                return permission_check

            serializer = FunctionsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'message': 'Ошибки валидации', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(
                {'message': 'Функция успешно создана', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception(f"Functions create error: {str(e)}")
            return Response(
                {'message': 'Ошибка создания функции'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        """Обновление функции"""
        try:
            # Проверка прав
            permission_check = self.check_permissions(request)
            if permission_check:
                return permission_check

            function_id = self.get_id_from_request(request)
            if not function_id:
                return Response(
                    {'message': 'ID функции обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            function = get_object_or_404(Functions, id=function_id)
            serializer = FunctionsSerializer(function, data=request.data, partial=True)
            
            if not serializer.is_valid():
                return Response(
                    {'message': 'Ошибки валидации', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(
                {'message': 'Функция успешно обновлена', 'data': serializer.data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"Functions update error: {str(e)}")
            return Response(
                {'message': 'Ошибка обновления функции'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """Удаление функции"""
        try:
            # Проверка прав
            permission_check = self.check_permissions(request)
            if permission_check:
                return permission_check

            function_id = self.get_id_from_request(request)
            if not function_id:
                return Response(
                    {'message': 'ID функции обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            function = get_object_or_404(Functions, id=function_id)
            function.delete()
            return Response(
                {'message': 'Функция успешно удалена'},
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            logger.exception(f"Functions delete error: {str(e)}")
            return Response(
                {'message': 'Ошибка удаления функции'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )