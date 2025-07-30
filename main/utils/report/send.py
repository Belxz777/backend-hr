from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from main.models import Functions
from main.serializer import ReportsSerializer
from main.utils.auth import get_user

logger = logging.getLogger('reports')

@api_view(['POST'])
@transaction.atomic
def create_report(request):
    """Создание отчета о выполненной работе"""
    logger.info(f"Report creation request from {request.META.get('REMOTE_ADDR')}")
    
    try:
        # 1. Аутентификация пользователя
        employee = get_user(request)
        if isinstance(employee, Response):
            return employee
        
        logger.debug(f"Authenticated employee: {employee.id}")

        # 2. Валидация входных данных
        required_fields = ['function_id', 'hours_worked']
        if not all(field in request.data for field in required_fields):
            logger.warning("Missing required fields")
            return Response(
                {'message': 'Необходимо указать function_id и hours_worked'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Проверка существования функции
        try:
            function = Functions.objects.get(id=request.data['function_id'])
            logger.debug(f"Found function: {function.name}")
        except ObjectDoesNotExist:
            logger.error(f"Function not found: {request.data['function_id']}")
            return Response(
                {'message': 'Указанная функция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 4. Проверка рабочего времени (0.5-10 часов)
        try:
            hours = float(request.data['hours_worked'])
            if not (0.5 <= hours <= 10):
                raise ValueError
        except (ValueError, TypeError):
            logger.warning(f"Invalid hours_worked: {request.data.get('hours_worked')}")
            return Response(
                {'message': 'Рабочее время должно быть от 0.5 до 10 часов'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Создание отчета
        report_data = {
            'by_employee': employee.id,
            'function': function.id,
            'hours_worked': hours,
            'comment': request.data.get('comment', '')
        }

        serializer = ReportsSerializer(data=report_data)
        if not serializer.is_valid():
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(
                {
                    'message': 'Ошибки валидации данных',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        report = serializer.save()
        logger.info(f"Created report ID: {report.id}")

        return Response(
            {
                'message': 'Отчет успешно создан',
                'data': {
                    'report_id': report.id,
                    'function': function.name,
                    'hours_worked': float(report.hours_worked),
                    'date': report.date.isoformat()
                }
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        logger.exception(f"Report creation error: {str(e)}")
        return Response(
            {'message': 'Ошибка при создании отчета'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )