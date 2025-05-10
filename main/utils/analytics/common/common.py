
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum,Q,Count,Value,CharField
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from main.models import Department, Employee, LaborCosts

@api_view(['GET'])
def get_all_departments_hours_report(request):
    try:
        # Get query parameters
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Check date parameters
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cache key construction
        # cache_key = f'dept_report_{date or ""}_{start_date or ""}_{end_date or ""}'
        # cached_data = cache.get(cache_key)
        
        # if cached_data:
        #     return Response(cached_data, status=status.HTTP_200_OK)

        # Build date filter
        date_filter = Q()
        
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

        departments = Department.objects.all()
        all_departments_data = []

        # Using prefetch_related to optimize queries
        labor_costs = LaborCosts.objects.select_related(
            'employee', 'department'
        ).filter(date_filter)

        for department in departments:
            dept_filter = date_filter & Q(department=department.departmentId)
            
            # Employee statistics with optimized query
            employee_stats = labor_costs.filter(
                department=department.departmentId
            ).values(
                'employee',
                'employee__firstName',
                'employee__lastName',
                'employee__patronymic',
            ).annotate(
                total_hours=Sum('worked_hours'),
                function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
                deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False))
            ).order_by('employee')

            # Department statistics
            department_stats = labor_costs.filter(
                department=department.departmentId
            ).aggregate(
                total_hours=Sum('worked_hours'),
                function_hours=Sum('worked_hours', filter=Q(function__isnull=False)),
                deputy_hours=Sum('worked_hours', filter=Q(deputy__isnull=False)),
                unique_employees=Count('employee', distinct=True)
            )

            # Daily statistics for date range
            daily_stats = []
            if time_period_type == 'range':
                daily_stats = labor_costs.filter(
                    department=department.departmentId
                ).values(
                    'date__date'
                ).annotate(
                    day_total=Sum('worked_hours'),
                    day_function=Sum('worked_hours', filter=Q(function__isnull=False)),
                    day_deputy=Sum('worked_hours', filter=Q(deputy__isnull=False))
                ).order_by('date__date')

            department_data = {
                'department_id': department.departmentId,
                'department_name': department.departmentName,
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
                        'employee_id': stat['employeeId'],
                        'first_name': stat['employeeId__firstName'],
                        'last_name': stat['employeeId__lastName'],
                        'patronymic': stat['employeeId__patronymic'],
                        'total_hours': float(stat['total_hours'] or 0),
                        'function_hours': float(stat['function_hours'] or 0),
                        'deputy_hours': float(stat['deputy_hours'] or 0)
                    }
                    for stat in employee_stats
                ]
            }

            if time_period_type == 'range':
                department_data['daily_stats'] = [
                    {
                        'date': stat['date__date'].strftime('%Y-%m-%d'),
                        'total_hours': float(stat['day_total'] or 0),
                        'function_hours': float(stat['day_function'] or 0),
                        'deputy_hours': float(stat['day_deputy'] or 0)
                    }
                    for stat in daily_stats
                ]
                department_data['time_period']['days_count'] = len(daily_stats)

            all_departments_data.append(department_data)

        response_data = {
            'departments': all_departments_data,
            'total_departments': len(all_departments_data)
        }


        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['GET'])
def get_top_duties_and_functions(request):
    try:
        # Получаем параметры запроса
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        limit = int(request.query_params.get('limit', 10))  # По умолчанию топ-10
        
        # Проверка параметров даты
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Строим фильтр по дате
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

        # Получаем общее количество часов для обязанностей и функций
        total_deputy_hours = float(LaborCosts.objects.filter(
            date_filter,
            deputy__isnull=False
        ).aggregate(total=Sum('worked_hours'))['total'] or 0)

        total_function_hours = float(LaborCosts.objects.filter(
            date_filter,
            function__isnull=False
        ).aggregate(total=Sum('worked_hours'))['total'] or 0)

        # Получаем топ обязанностей (Deputy)
        top_deputies = LaborCosts.objects.filter(
            date_filter,
            deputy__isnull=False
        ).values(
            'deputy__deputyId',
            'deputy__deputyName'
        ).annotate(
            total_hours=Sum('worked_hours'),
            count=Count('deputy')
        ).order_by('-total_hours')[:limit]

        # Получаем топ функций (Functions)
        top_functions = LaborCosts.objects.filter(
            date_filter,
            function__isnull=False
        ).values(
            'function__funcId',
            'function__funcName'
        ).annotate(
            total_hours=Sum('worked_hours'),
            count=Count('function')
        ).order_by('-total_hours')[:limit]

        # Формируем ответ с процентами
        response_data = {
            'top_deputies': [
                {
                    'deputy_id': item['deputy__deputyId'],
                    'deputy_name': item['deputy__deputyName'],
                    'total_hours': float(item['total_hours'] or 0),
                    'percentage': float(round((float(item['total_hours'] or 0) / total_deputy_hours * 100), 2) if total_deputy_hours > 0 else 0),
                    'count': item['count']
                }
                for item in top_deputies
            ],
            'top_functions': [
                {
                    'function_id': item['function__funcId'],
                    'function_name': item['function__funcName'],
                    'total_hours': float(item['total_hours'] or 0),
                    'percentage': float(round((float(item['total_hours'] or 0) / total_function_hours * 100), 2) if total_function_hours > 0 else 0),
                    'count': item['count']
                }
                for item in top_functions
            ],
            'summary': {
                'total_deputy_hours': total_deputy_hours,
                'total_function_hours': total_function_hours,
                'time_period': {
                    'date': date if date else None,
                    'start_date': start_date if start_date else None,
                    'end_date': end_date if end_date else None
                }
            }
        
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['GET'])
def get_combined_top_duties_and_functions(request):
    try:
        # Получаем параметры запроса
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        limit = int(request.query_params.get('limit', 10))  # По умолчанию топ-10
        
        # Проверка параметров даты
        if not date and not (start_date and end_date):
            return Response(
                {'error': 'Укажите либо date, либо start_date и end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Строим фильтр по дате
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

        # Получаем общее количество часов для всех записей
        total_all_hours = float(LaborCosts.objects.filter(
            date_filter
        ).aggregate(total=Sum('worked_hours'))['total'] or 0)

        # Получаем топ обязанностей (Deputy)
        top_deputies = LaborCosts.objects.filter(
            date_filter,
            deputy__isnull=False
        ).values(
            'deputy__deputyId',
            'deputy__deputyName'
        ).annotate(
            total_hours=Sum('worked_hours'),
            count=Count('deputy'),
            type=Value('deputy', output_field=CharField())  # Добавляем тип записи
        ).order_by('-total_hours')

        # Получаем топ функций (Functions)
        top_functions = LaborCosts.objects.filter(
            date_filter,
            function__isnull=False
        ).values(
            'function__funcId',
            'function__funcName'
        ).annotate(
            total_hours=Sum('worked_hours'),
            count=Count('function'),
            type=Value('function', output_field=CharField())  # Добавляем тип записи
        ).order_by('-total_hours')

        # Объединяем и сортируем вместе
        combined_top = list(top_deputies) + list(top_functions)
        combined_top_sorted = sorted(
            combined_top, 
            key=lambda x: float(x['total_hours'] or 0), 
            reverse=True
        )[:limit]

        # Формируем ответ с процентами от общего количества часов
        response_data = {
            'top_items': [
                {
                    'id': item['deputy__deputyId'] if item['type'] == 'deputy' else item['function__funcId'],
                    'name': item['deputy__deputyName'] if item['type'] == 'deputy' else item['function__funcName'],
                    'total_hours': float(item['total_hours'] or 0),
                    'percentage': round(float(item['total_hours'] or 0) / total_all_hours * 100, 2) if total_all_hours > 0 else 0,
                    'count': item['count'],
                    'type': item['type']
                }
                for item in combined_top_sorted
            ],
            'summary': {
                'total_all_hours': total_all_hours,
                'time_period': {
                    'date': date if date else None,
                    'start_date': start_date if start_date else None,
                    'end_date': end_date if end_date else None
                }
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Ошибка сервера: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )