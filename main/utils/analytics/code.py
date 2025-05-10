from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum,Q,Count
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from main.models import Department, Employee, LaborCosts

@api_view(['GET'])
def get_department_hours_report(request):
    try:
        # Получаем параметры запроса
        department_id = request.query_params.get('department_id')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Проверяем обязательные параметры
        if not department_id:
            return Response(
                {'error': 'Параметр department_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        department = Department.objects.filter(departmentId=department_id).values('departmentName')
        print(department)
        # Проверяем, что передана либо конкретная дата, либо период
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Строим фильтр по дате
        date_filter = Q(department=department_id)
        
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d').date()
                date_filter &= Q(date__date=target_date)
                time_period_type = 'single_day'
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
                time_period_type = 'range'
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Базовый запрос для статистики по сотрудникам
        employee_stats = LaborCosts.objects.select_related('employee').filter(date_filter).values(
            'employee',
            'employee__firstName',
            'employee__lastName',
            'employee__patronymic',
        ).annotate(
            total_hours=Sum('worked_hours'),
            function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
            deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False))
        ).order_by('employee')
        
        # Общая статистика по отделу
        department_stats = LaborCosts.objects.filter(date_filter).aggregate(
            total_hours=Sum('worked_hours'),
            function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
            deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False)),
            unique_employees=Count('employee', distinct=True)
        )
        
        # Дополнительная статистика по дням, если выбран период
        daily_stats = []
        if time_period_type == 'range':
            daily_stats = LaborCosts.objects.filter(date_filter).values(
                'date__date'
            ).annotate(
                day_total=Sum('worked_hours'),
                day_function=Sum('worked_hours', filter=Q(function__isnull=False)),
                day_deputy=Sum('worked_hours', filter=Q(deputy__isnull=False))
            ).order_by('date__date')
        
        # Формируем ответ
        response_data = {
            'department_id': department_id,
            'department_name':department.first()['departmentName'],
            'time_period': {
                'type': time_period_type,
                'date': date if time_period_type == 'single_day' else None,
                'start_date': start_date if time_period_type == 'range' else None,
                'end_date': end_date if time_period_type == 'range' else None,
            },
            'department_stats': {
                'total_hours': float(department_stats['total_hours'] or 0),
                'function_hours': float(department_stats['function_hours'] or 0),
                'deputy_hours': float(department_stats['deputy_hours'] or 0),
                'employee_count': department_stats['unique_employees'] or 0
            },
            'employee_stats': [
                {
                    'employee_id': stat['employee'],
                    'first_name': stat['employee__firstName'],
                    'last_name': stat['employee__lastName'],
                    'patronymic': stat['employee__patronymic'],
                    'total_hours': float(stat['total_hours'] or 0),
                    'function_hours': float(stat['function_hours'] or 0),
                    'deputy_hours': float(stat['deputy_hours'] or 0)
                }
                for stat in employee_stats
            ]
        }
        
        if time_period_type == 'range':
            response_data['daily_stats'] = [
                {
                    'date': stat['date__date'].strftime('%Y-%m-%d'),
                    'total_hours': float(stat['day_total'] or 0),
                    'function_hours': float(stat['day_function'] or 0),
                    'deputy_hours': float(stat['day_deputy'] or 0)
                }
                for stat in daily_stats
            ]
            response_data['time_period']['days_count'] = len(daily_stats)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['GET'])
def get_employee_hours_report(request):
    try:
        # Получаем параметры запроса
        employee_id = request.query_params.get('employee_id')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Проверяем обязательные параметры
        if not employee_id:
            return Response(
                {'error': 'Параметр employee_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверяем, что передана либо конкретная дата, либо период
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Строим фильтр по дате
        employee = Employee.objects.filter(employeeId=employee_id).first()
        date_filter = Q()
        
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
        
        # Получаем все записи сотрудника
        time_entries = LaborCosts.objects.filter(
            Q(employee=employee_id) & date_filter
        ).values(
            'laborCostId',
            'department',
            'function',
            'deputy',
            'compulsory',
            'worked_hours',
            'comment',
            'date'
        ).order_by('date')
        
        # Группируем данные по типам задач
        summary = LaborCosts.objects.filter(
            Q(employee=employee_id) & date_filter
        ).aggregate(
            total_hours=Sum('worked_hours'),
            function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
            deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False)),
            compulsory_hours=Sum('worked_hours', filter=Q(compulsory=True)),
            non_compulsory_hours=Sum('worked_hours', filter=Q(compulsory=False))
        )
        
        # Дополнительная группировка по дням, если выбран период
        daily_summary = []
        if start_date and end_date:
            daily_data = LaborCosts.objects.filter(
                Q(employee=employee_id) & date_filter
            ).values('date__date').annotate(
                day_total=Sum('worked_hours'),
                day_function=Sum('worked_hours', filter=Q(function__isnull=False)),
                day_deputy=Sum('worked_hours', filter=Q(deputy__isnull=False))
            ).order_by('date__date')
            
            daily_summary = [
                {
                    'date': entry['date__date'].strftime('%Y-%m-%d'),
                    'total_hours': float(entry['day_total']) if entry['day_total'] else 0.0,
                    'function_hours': float(entry['day_function']) if entry['day_function'] else 0.0,
                    'deputy_hours': float(entry['day_deputy']) if entry['day_deputy'] else 0.0
                }
                for entry in daily_data
            ]
        
        # Преобразуем None в 0 для агрегированных значений
        for key in summary:
            if summary[key] is None:
                summary[key] = 0.0
        
        response_data = {
            'employee': {
                'employee_id': employee_id,
                'employee_name': employee.firstName,
              'employee_surname': employee.lastName,
              'employee_patronymic': employee.patronymic,
            },
            'summary': summary,
            'reports': list(time_entries),
            'reports_count': len(time_entries),
            'query_params': {
                'date': date,
                'start_date': start_date,
                'end_date': end_date
            }
        }
        
        if start_date and end_date:
            response_data['daily_summary'] = daily_summary
            response_data['period'] = {
                'start_date': start_date,
                'end_date': end_date,
                'days_count': len(daily_summary)
            }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )