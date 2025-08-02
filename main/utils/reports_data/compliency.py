from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from main.models import Employee, Reports, Department, Functions
import logging
logger = logging.getLogger(__name__)

class EmployeePerformanceView(APIView):
    def get(self, request):
        """Получение данных о производительности сотрудника с полной информацией о времени"""
        try:
            # 1. Получение и валидация параметров
            employee_id = request.query_params.get("emp_id")
            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            if not employee_id:
                logger.warning("Missing employee_id parameter")
                return Response(
                    {"message": "Необходимо указать emp_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Проверка существования сотрудника
            try:
                employee = Employee.objects.get(id=employee_id)
                logger.debug(f"Employee found: {employee.surname} {employee.name}")
            except Employee.DoesNotExist:
                logger.error(f"Employee not found: {employee_id}")
                return Response(
                    {"message": "Сотрудник не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # 3. Обработка диапазона дат (включая end_date)
            today = timezone.now().date()
            
            if start_date_str and end_date_str:
                try:
                    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    end_date_plus_1 = end_date + timedelta(days=1)
                    
                    if start_date > end_date:
                        return Response(
                            {"message": "Дата начала не может быть позже даты окончания"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                        
                except ValueError:
                    logger.warning("Invalid date format")
                    return Response(
                        {"message": "Неверный формат даты. Используйте YYYY-MM-DD"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                # По умолчанию - последние 30 дней (включая сегодня)
                end_date = today
                start_date = end_date - timedelta(days=29)
                end_date_plus_1 = end_date + timedelta(days=1)

            logger.debug(f"Date range for employee {employee_id}: {start_date} to {end_date} (inclusive)")

            # 4. Получение отчетов с учетом часового пояса
            reports = Reports.objects.filter(
                by_employee=employee,
                date__gte=start_date,
                date__lt=end_date_plus_1  # Используем строго меньше следующего дня
            ).select_related('function', 'by_employee__department').order_by('date')

            # 5. Формирование структуры ответа
            response_data = {
                "employee_id": employee.id,
                "employee_name": f"{employee.surname} {employee.name}",
                "department_name": employee.department.name,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_hours": 0.0,
                "reports_by_date": {},
            }

            total_hours = 0.0
            for report in reports:
                date_key = report.date.strftime('%Y-%m-%d')
                full_datetime = report.date.isoformat()
                hours = float(report.hours_worked)
                total_hours += hours

                # Группировка по датам
                if date_key not in response_data["reports_by_date"]:
                    response_data["reports_by_date"][date_key] = []
                
                response_data["reports_by_date"][date_key].append({
                    "report_id": report.id,
                    "function_id": report.function.id,
                    "function_name": report.function.name,
                    "hours_worked": hours,
                    "comment": report.comment,
                    "date": full_datetime
                })

                # Подробные отчеты с полной датой
               

            response_data["total_hours"] = round(total_hours, 2)

            # 6. Формирование ответа
     
            return Response(
                {"data": response_data},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"Error in EmployeePerformanceView: {str(e)}")
            return Response(
                {
                    "message": "Ошибка при получении данных о производительности",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )