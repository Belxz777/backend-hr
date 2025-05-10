from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q, Count, F
from datetime import datetime
from main import models
from main.models import Department, Deputy, Employee, LaborCosts, Functions

@api_view(['GET'])
def get_tasks_distribution(request):
    try:
        # Получаем параметры запроса
        date = request.query_params.get('date')
        department_id = request.query_params.get('department_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not department_id:
            return Response(
                {'error': 'Параметр department_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        department = Department.objects.filter(departmentId=department_id).values('departmentName')
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
        
        # 1. Считаем общее время всех отчетов
        total_stats = LaborCosts.objects.filter(date_filter).aggregate(
            total_hours=Sum('worked_hours'),
            total_function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
            total_deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False)),
            total_compulsory_hours=Sum('worked_hours', filter=Q(compulsory=True)),
            total_non_compulsory_hours=Sum('worked_hours', filter=Q(compulsory=False)),
            total_typical_hours=Sum('worked_hours', filter=Q(function__consistent__isnull=False)),
            total_non_typical_hours=Sum('worked_hours', filter=Q(function__consistent__isnull=True))
         )
        
        # Преобразуем None в 0
        total_hours = float(total_stats['total_hours'] or 0)
        
        # Если нет данных
        if total_hours == 0:
            return Response({
                'department_id': department_id,
            'department_name':department.first()['departmentName'],
                'message': 'Нет данных за указанный период',
                'total_hours': 0,
                'distribution': {}
            }, status=status.HTTP_200_OK)
        # ! продумать логику вывода 
        # 2. Считаем распределение по функциям (типовым и нетиповым)
        function_distribution = LaborCosts.objects.filter(
            date_filter & Q(function__isnull=False)
        ).select_related('function').values(
            'function_id',
            'function__funcName',
            'function__consistent'  # Для разделения на типовые/нетиповые
        ).annotate(
            hours=Sum('worked_hours'),
            count=Count('laborCostId')
        ).order_by('-hours')
        
        # 3. Считаем распределение по замещениям
        deputy_distribution = LaborCosts.objects.filter(
            date_filter & Q(deputy__isnull=False)
        ).select_related('deputy').values(
            'deputy_id',
            'deputy__deputyName'
        ).annotate(
            hours=Sum('worked_hours'),
            count=Count('laborCostId')
        ).order_by('-hours')
        
        # 4. Формируем итоговый отчет
        distribution = {
            'by_type': {
                'functions': {
                    'hours': float(total_stats['total_function_hours'] or 0),
                    'percent': round(float(total_stats['total_function_hours'] or 0) / total_hours * 100, 2)
                },
                'deputies': {
                    'hours': float(total_stats['total_deputy_hours'] or 0),
                    'percent': round(float(total_stats['total_deputy_hours'] or 0) / total_hours * 100, 2)
                },
                'compulsory': {
                    'hours': float(total_stats['total_compulsory_hours'] or 0),
                    'percent': round(float(total_stats['total_compulsory_hours'] or 0) / total_hours * 100, 2)
                },
                'non_compulsory': {
                    'hours': float(total_stats['total_non_compulsory_hours'] or 0),
                    'percent': round(float(total_stats['total_non_compulsory_hours'] or 0) / total_hours * 100, 2)
                },
                'typical': {
                    'hours': float(total_stats['total_typical_hours'] or 0),
                    'percent': round(float(total_stats['total_typical_hours'] or 0) / total_hours * 100, 2)
                },
                'non_typical': {
                    'hours': float(total_stats['total_non_typical_hours'] or 0),
                    'percent': round(float(total_stats['total_non_typical_hours'] or 0) / total_hours * 100, 2)
                }
            },
            'by_functions': {
                'typical': [],
                'non_typical': []
            },
            'by_deputies': []
        }
        
        # Добавляем распределение по конкретным функциям (разделяем на типовые и нетиповые)
        for func in function_distribution:
            func_hours = float(func['hours'] or 0)
            func_data = {
                'function_id': func['function_id'],
                'function_name': func['function__funcName'],
                'hours': func_hours,
                'percent': round(func_hours / total_hours * 100, 2),
                'entries_count': func['count']
            }
            
            if func['function__consistent'] is None:
                distribution['by_functions']['non_typical'].append(func_data)
            else:
                distribution['by_functions']['typical'].append(func_data)
        
        # Добавляем распределение по конкретным замещениям
        for dep in deputy_distribution:
            dep_hours = float(dep['hours'] or 0)
            distribution['by_deputies'].append({
                'deputy_id': dep['deputy_id'],
                'deputy_name': dep['deputy__deputyName'],
                'hours': dep_hours,
                'percent': round(dep_hours / total_hours * 100, 2),
                'reports_count': dep['count']
            })

        # Формируем полный ответ
        response_data = {
            'department_id': department_id,
            'department_name':department.first()['departmentName'],
            'time_period': {
                'type': time_period_type,
                'date': date if time_period_type == 'single_day' else None,
                'start_date': start_date if time_period_type == 'range' else None,
                'end_date': end_date if time_period_type == 'range' else None,
            },
            'total_hours': total_hours,
            'total_entries': LaborCosts.objects.filter(date_filter).count(),
            'distribution': distribution
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
@api_view(['GET'])
def get_employee_tasks_distribution(request):
    try:
        # Получаем обязательные параметры
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response(
                {'error': 'Параметр employee_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Получаем параметры даты
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Проверяем период времени
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем сотрудника и его должность с обязанностями
        try:
            employee = Employee.objects.select_related('jobid', 'jobid__deputy').get(employeeId=employee_id)
             
            employee_deputy = employee.jobid.deputy if employee.jobid else None
            employee_typical = Functions.objects.filter(consistent = employee_deputy.deputyId)
            print(
                  employee_typical)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Сотрудник не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Строим базовый фильтр
        base_filter = Q(employee=employee_id)
        
        # Добавляем фильтр по дате
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d').date()
                base_filter &= Q(date__date=target_date)
                time_period_type = 'single_day'
                days_count = 1
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                base_filter &= Q(date__date__range=[start, end])
                time_period_type = 'range'
                days_count = (end - start).days + 1
            except ValueError:
                return Response(
                    {'error': 'Неверный формат даты. Используйте YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Аннотируем функции проверкой на принадлежность к обязанностям должности
        from django.db.models import Exists, OuterRef

        function_distribution = LaborCosts.objects.filter(
            base_filter & Q(function__isnull=False)
        ).select_related('function').values(
            'function_id',
            'function__funcName',
            'function__consistent',
        ).annotate(
            hours=Sum('worked_hours'),
            count=Count('laborCostId')
        ).order_by('-hours')
    
        # Инициализируем структуру распределения
        distribution = {
            'by_functions': {
                'typical': [],
                'non_typical': []
            },
            'extra': []
        }

        # Вычисляем общее количество часов
        total_hours = sum(float(func['hours'] or 0) for func in function_distribution)

        # Получаем список ID типичных функций сотрудника
        typical_function_ids = set(employee_typical.values_list('funcId', flat=True))

        # Добавляем распределение по функциям
        # Calculate total hours including both functions and deputy hours
        deputies = LaborCosts.objects.filter(
            base_filter & Q(function__isnull=True) & Q(deputy__isnull=False) & Q(compulsory=False)
        ).select_related('deputy').values(
            'deputy__deputyName',
            'deputy__deputyId',
            'worked_hours'
        ).annotate(
            total_hours=Sum('worked_hours')
        )
    
        total_combined_hours = float(total_hours) + float(sum(deputy['total_hours'] for deputy in deputies))

        for func in function_distribution:
            func_hours = float(func['hours'] or 0)
            func_data = {
                'function_id': func['function_id'],
                'function_name': func['function__funcName'],
                'hours': func_hours,
                'percent': round(float(func_hours) / float(total_combined_hours) * 100, 2) if total_combined_hours > 0 else 0,
                'entries_count': func['count']
            }
            
            if func['function_id'] in typical_function_ids:
                distribution['by_functions']['typical'].append(func_data)
            else:
                distribution['by_functions']['non_typical'].append(func_data)     
                
        deputy_hours = float(sum(deputy['total_hours'] for deputy in deputies))
        for deputy in deputies:
            deputy_total_hours = float(deputy['total_hours'])
            distribution['extra'].append({
                'type': 'deputy',
                'deputy_id': deputy['deputy__deputyId'],
                'deputy_name': deputy['deputy__deputyName'],
                'hours': deputy_total_hours,
                'percent': round(deputy_total_hours / float(total_combined_hours) * 100, 2) if total_combined_hours > 0 else 0,
                'entries_count': 1,
            })        
        response_data = {
            'employee': {
                'employee_id': employee_id,
                'employee_name': employee.firstName,
              'employee_surname': employee.lastName,
              'employee_patronymic': employee.patronymic,
            },
            'time_period': {
                'type': time_period_type,
                'date': date if time_period_type == 'single_day' else None,
                'start_date': start_date if time_period_type == 'range' else None,
                'end_date': end_date if time_period_type == 'range' else None,
            },
            'total_hours': total_hours,
        #    'typical': [{'function_id': func.funcId, 'function_name': func.funcName} for func in employee_typical],        
            'total_reports': LaborCosts.objects.filter(base_filter).count(),
            'distribution': distribution
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )