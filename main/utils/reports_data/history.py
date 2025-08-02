from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

import logging

from main.models import Department, Reports


logger = logging.getLogger(__name__)

class DepartmentPerformanceView(APIView):
    def get(self, request):
        """Получение статистики производительности отдела с полными датами"""
        try:
            # 1. Получаем и валидируем параметры
            department_id = request.query_params.get("department_id")
            if not department_id:
                logger.warning("Missing department_id parameter")
                return Response(
                    {"message": "Необходимо указать department_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Проверяем существование отдела
            try:
                department = Department.objects.get(id=department_id)
                logger.debug(f"Found department: {department.name}")
            except Department.DoesNotExist:
                logger.error(f"Department not found: {department_id}")
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
                        raise ValidationError("Дата начала периода не может быть позже даты окончания")
                    if start_date > today:
                        raise ValidationError("Дата начала периода не может быть в будущем")
                except ValueError as e:
                    logger.warning(f"Invalid date format: {str(e)}")
                    return Response(
                        {"message": "Неверный формат даты. Используйте YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                end_date = today
                start_date = end_date - timedelta(days=29)
                end_date_plus_1 = end_date + timedelta(days=1)

            # 4. Получаем отчеты с полной датой и временем
            reports = Reports.objects.filter(
                by_employee__department=department_id,
                date__gte=start_date,
                date__lt=end_date_plus_1
            ).select_related('by_employee', 'function').order_by('date')

            # 5. Формируем структуру ответа
            response_data = {
                "department_id": department.id,
                "department_name": department.name,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_hours": 0.0,
                "reports_by_date": {}  # Используем обычный dict вместо defaultdict
            }

            total_hours = 0.0
            for report in reports:
                date_key = report.date.strftime('%Y-%m-%d')
                full_datetime = report.date.isoformat()  # Полная дата и время
                hours = float(report.hours_worked)
                total_hours += hours

                if date_key not in response_data["reports_by_date"]:
                    response_data["reports_by_date"][date_key] = []
                
                response_data["reports_by_date"][date_key].append({
                    "report_id": report.id,
                    "employee_id": report.by_employee.id,
                    "employee_name": f"{report.by_employee.surname} {report.by_employee.name}",
                    "function_id": report.function.id,
                    "function_name": report.function.name,
                    "hours_worked": hours,
                    "comment": report.comment,
                    "date": full_datetime,  # Полная дата и время создания
                })

            response_data["total_hours"] = round(total_hours, 2)

            # Преобразуем в обычный dict перед возвратом
            response_data["reports_by_date"] = dict(response_data["reports_by_date"])

            return Response(
                {
                    "message": "Данные о производительности отдела",
                    "data": response_data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"Error in DepartmentPerformanceView: {str(e)}")
            return Response(
                {"message": "Ошибка при получении данных о производительности"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )