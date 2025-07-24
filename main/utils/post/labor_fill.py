from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from main.models import Deputy, Employee, LaborCosts,Functions
from main.serializer import LaborCostsSerializer
from main.utils.auth import get_user
from main.utils.closeDate import isExpired
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from main.models import Employee, Functions, Deputy, LaborCosts
from main.utils.auth import get_user

logger = logging.getLogger(__name__)

@api_view(['POST'])
def labor_fill(request):
    logger.info(f"Starting labor_fill request from {request.META.get('REMOTE_ADDR')}")
    
    try:
        # Аутентификация пользователя
        employee = get_user(request)
        if not employee:
            logger.warning(f"Unauthorized labor_fill attempt from IP: {request.META.get('REMOTE_ADDR')}")
            return Response(
                {"error": "Рабочий под таким номером не существует"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        logger.debug(f"Authenticated employee: {employee.employeeId}")

        # Валидация входных данных
        data = request.data
        function_id = data.get('func_id')
        deputy_id = data.get('deputy_id')
        
        if function_id is None and deputy_id is None:
            logger.warning(f"Missing both func_id and deputy_id for employee {employee.employeeId}")
            return Response(
                {"error": "Не указана функция или deputy"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получение функции или deputy
        try:
            if function_id:
                function = Functions.objects.get(funcId=function_id)
                logger.debug(f"Found function: {function.funcName} (ID: {function.funcId})")
            elif deputy_id:
                deputy = Deputy.objects.get(deputyId=deputy_id)
                logger.debug(f"Found deputy: {deputy.deputyName} (ID: {deputy.deputyId})")
        except ObjectDoesNotExist:
            logger.error(f"Function or deputy not found (func_id: {function_id}, deputy_id: {deputy_id})")
            return Response(
                {"error": "Функция или deputy не найдены"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверка рабочего времени
        working_hours = data.get('workingHours')
        if not working_hours or not isinstance(working_hours, (int, float)) or working_hours <= 0:
            logger.warning(f"Invalid workingHours value: {working_hours}")
            return Response(
                {"error": "Некорректное значение рабочего времени"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создание записи о трудозатратах
        try:
            if function_id:
                labor_cost = LaborCosts.objects.create(
                    employee=employee,
                    department=employee.departmentid,
                    function=function,
                    worked_hours=working_hours,
                    comment=data.get('comment', '')
                )
            else:
                labor_cost = LaborCosts.objects.create(
                    employee=employee,
                    department=employee.departmentid,
                    deputy=deputy,
                    compulsory=False,
                    worked_hours=working_hours,
                    comment=data.get('comment', '')
                )
                
            logger.info(f"Successfully created labor cost record (ID: {labor_cost.id})")
            return Response(
                {'message': 'Запись о проделанной работе создана. Хорошего вам дня!'}, 
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.exception(f"Error creating labor cost record: {str(e)}")
            return Response(
                {'error': 'Ошибка при создании записи'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        logger.exception(f"Unexpected error in labor_fill: {str(e)}")
        return Response(
            {'error': 'Внутренняя ошибка сервера'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_user(request, id):
    logger.info(f"Starting delete_user request for employee ID: {id}")
    
    try:
        # Проверка валидности ID
        if not id or not str(id).isdigit():
            logger.warning(f"Invalid employee ID format: {id}")
            return Response(
                {'error': 'Некорректный ID сотрудника'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Поиск и удаление пользователя
        user = Employee.objects.filter(employeeId=id).first()
        if not user:
            logger.warning(f"Employee not found for deletion (ID: {id})")
            return Response(
                {'error': 'Сотрудник не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        user.delete()
        logger.info(f"Successfully deleted employee (ID: {id})")
        return Response(
            {'message': 'Сотрудник удален'}, 
            status=status.HTTP_204_NO_CONTENT
        )

    except Exception as e:
        logger.exception(f"Error deleting employee (ID: {id}): {str(e)}")
        return Response(
            {'error': 'Ошибка при удалении сотрудника'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
