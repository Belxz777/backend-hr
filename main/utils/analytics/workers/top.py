
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum,Q,Count,Value,CharField
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from main.models import Department,Employee, LaborCosts

@api_view(['GET'])
def get_top_employees_by_department(request):
    try:
        # Получаем параметры запроса
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        department_id = request.query_params.get('department_id')
        end_date = request.query_params.get('end_date')
        limit_per_dept = int(request.query_params.get('limit', 5))  # По умолчанию топ-5 на отдел
        
        # Проверка параметров даты
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Строим фильтр по дате
        date_filter = Q()
        
        if department_id:
            date_filter &= Q(department_id=department_id)
        
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d').date()
                date_filter &= Q(date__date=target_date)
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                date_filter &= Q(date__date__range=[start, end])
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Получаем отделы
        departments = Department.objects.all()
        if department_id:
            departments = departments.filter(departmentId=department_id)
            
        result = {}

        for department in departments:
            # Получаем топ сотрудников отдела
            top_employees = LaborCosts.objects.filter(
                date_filter,
                department=department
            ).select_related('employee').values(
                'employee_id',
                'employee__firstName',
                'employee__lastName',
                'employee__patronymic',
                'employee__jobid__jobName'
            ).annotate(
                total_hours=Sum('worked_hours'),
                function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
                deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False))
            ).order_by('-total_hours')[:limit_per_dept]

            # Добавляем в результат
            result[department.departmentName] = {
                'department_id': department.departmentId,
                'top_employees': [
                    {
                        'employee_id': emp['employee_id'],
                        'full_name': f"{emp['employee__lastName']} {emp['employee__firstName']} {emp['employee__patronymic']}",
                        'job_title': emp['employee__jobid__jobName'],
                        'total_hours': float(emp['total_hours'] or 0),
                        'function_hours': float(emp['function_hours'] or 0),
                        'deputy_hours': float(emp['deputy_hours'] or 0)
                    }
                    for emp in top_employees
                ]
            }
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )