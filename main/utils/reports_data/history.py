from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

import logging

from main.models import Department, Reports

logger = logging.getLogger('performance')

class DepartmentPerformanceView(APIView):
    def get(self, request):
        """Получение статистики производительности отдела за указанный период или последние 30 дней по умолчанию"""
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

            # 3. Получаем параметры дат или устанавливаем по умолчанию (последние 30 дней)
            today = timezone.now().date()
            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            if start_date_str and end_date_str:
                try:
                    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    
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
                except ValidationError as e:
                    logger.warning(f"Invalid date range: {str(e)}")
                    return Response(
                        {"message": str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # По умолчанию - последние 30 дней
                end_date = today
                start_date = end_date - timedelta(days=30)

            logger.debug(f"Date range: {start_date} to {end_date}")

            reports = Reports.objects.filter(
                by_employee__department=department_id,
                date__gte=start_date,
                date__lte=end_date
            ).select_related('by_employee', 'function').order_by('date')

            if not reports.exists():
                logger.info(f"No reports found for department {department_id}")
                return Response(
                    {
                        "message": "Нет данных за указанный период",
                        "data": {
                            "department_id": department_id,
                            "department_name": department.name,
                            "start_date": start_date,
                            "end_date": end_date,
                            "reports": []
                        }
                    },
                    status=status.HTTP_200_OK
                )

            # 5. Формируем структуру ответа
            performance_data = {
                "department_id": department.id,
                "department_name": department.name,
                "start_date": start_date,
                "end_date": end_date,
                "total_hours": sum(float(r.hours_worked) for r in reports),
                "reports_by_date": {}
            }

            for report in reports:
                date_str = report.date.strftime('%Y-%m-%d')
                if date_str not in performance_data["reports_by_date"]:
                    performance_data["reports_by_date"][date_str] = []
                
                performance_data["reports_by_date"][date_str].append({
                    "report_id": report.id,
                    "employee_id": report.by_employee.id,
                    "employee_name": f"{report.by_employee.surname} {report.by_employee.name}",
                    "function_id": report.function.id,
                    "function_name": report.function.name,
                    "hours_worked": float(report.hours_worked),
                    "comment": report.comment
                })

            logger.info(f"Returning performance data for department {department_id}")
            return Response(
                {
                    "message": "Данные о производительности отдела",
                    "data": performance_data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"Error in DepartmentPerformanceView: {str(e)}")
            return Response(
                {"message": "Ошибка при получении данных о производительности"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )