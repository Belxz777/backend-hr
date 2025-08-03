from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator,EmptyPage
import logging

from main.models import Department, Employee, Reports


logger = logging.getLogger(__name__)
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import logging
from collections import defaultdict

# Предполагаемые модели (замените на ваши реальные модели)

logger = logging.getLogger(__name__)
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.cache import cache
from collections import defaultdict
import logging
import hashlib

# Предполагаемые модели
logger = logging.getLogger(__name__)

class DepartmentPerformanceView(APIView):
    def _generate_cache_key(self, request):
        """Генерация уникального ключа кэша на основе параметров запроса"""
        params = {
            'department_id': request.query_params.get("department_id"),
            'start_date': request.query_params.get("start_date"),
            'end_date': request.query_params.get("end_date"),
            'page': request.query_params.get("page", "1"),
            'page_size': request.query_params.get("page_size", "20")
        }
        param_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()) if v)
        return f"dept_perf:{hashlib.md5(param_string.encode()).hexdigest()}"

    def get(self, request):
        """Получение всех отчетов отдела с пагинацией и кэшированием"""
        cache_key = self._generate_cache_key(request)
        cached_response = cache.get(cache_key)
        
        if cached_response is not None:
            logger.debug("Возвращаем кэшированные данные")
            return Response(cached_response['data'], status=cached_response['status'])

        try:
            # 1. Валидация параметров
            department_id = request.query_params.get("department_id")
            if not department_id:
                return Response(
                    {"message": "Необходимо указать department_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Параметры пагинации
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("page_size", 20))
            if page < 1 or page_size < 1:
                return Response(
                    {"message": "Некорректные параметры пагинации"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Проверка существования отдела
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return Response(
                    {"message": "Отдел не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 3. Обработка дат
            today = timezone.now().date()
            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            if start_date_str and end_date_str:
                try:
                    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    end_date_plus_1 = end_date + timedelta(days=1)
                    
                    if start_date > end_date:
                        raise ValidationError("Дата начала не может быть позже даты окончания")
                except ValueError:
                    return Response(
                        {"message": "Неверный формат даты. Используйте YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                end_date = today
                start_date = end_date - timedelta(days=29)
                end_date_plus_1 = end_date + timedelta(days=1)

            # 4. Получаем все отчеты отдела за период
            reports = Reports.objects.filter(
                by_employee__department=department_id,
                date__gte=start_date,
                date__lt=end_date_plus_1
            ).select_related('by_employee', 'function').order_by('-date')

            # 5. Пагинация отчетов
            paginator = Paginator(reports, page_size)
            
            try:
                reports_page = paginator.page(page)
            except EmptyPage:
                return Response(
                    {"message": "Страница не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 6. Формируем структуру ответа (полностью сохраняем оригинальные имена)
            response_data = {
                "department_id": department.id,
                "department_name": department.name,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "pagination": {
                    "current_page": page,
                    "page_size": page_size,
                    "total_reports": paginator.count,
                    "total_pages": paginator.num_pages,
                    "has_next": reports_page.has_next(),
                    "has_previous": reports_page.has_previous(),
                },
                "reports_by_date": defaultdict(list),
                "total_hours": 0.0
            }

            total_hours = 0.0
            
            for report in reports_page:
                date_key = report.date.strftime('%Y-%m-%d')
                hours = float(report.hours_worked)
                total_hours += hours

                response_data["reports_by_date"][date_key].append({
                    "report_id": report.id,
                    "employee_id": report.by_employee.id,
                    "employee_name": f"{report.by_employee.surname} {report.by_employee.name}",
                    "function": {
                        "id": report.function.id if report.function else None,
                        "name": report.function.name if report.function else None
                    },
                    "hours_worked": hours,
                    "comment": report.comment,
                    "full_date": report.date.isoformat()
                })

            response_data["total_hours"] = round(total_hours, 2)
            response_data["reports_by_date"] = dict(response_data["reports_by_date"])

            # 7. Добавляем URL для навигации
            base_url = request.build_absolute_uri().split('?')[0]
            params = {
                "department_id": department_id,
                "page_size": page_size,
                "start_date": start_date_str or start_date.isoformat(),
                "end_date": end_date_str or end_date.isoformat()
            }

            if reports_page.has_next():
                response_data["pagination"]["next_page"] = (
                    f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
                    f"&page={page + 1}"
                )

            if reports_page.has_previous():
                response_data["pagination"]["previous_page"] = (
                    f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
                    f"&page={page - 1}"
                )

            # Формируем полный ответ для кэширования
            api_response = {
                "message": "Отчеты отдела",
                "data": response_data
            }

            # Кэшируем ответ на 5 минут (300 секунд)
            cache.set(cache_key, {
                'data': api_response,
                'status': status.HTTP_200_OK
            }, timeout=300)

            return Response(api_response, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Ошибка в DepartmentPerformanceView: {str(e)}")
            return Response(
                {"message": "Ошибка сервера при получении отчетов"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )