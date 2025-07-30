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
        """Get employee performance data for a specified period or last 30 days by default"""
        try:
            # Get parameters
            employee_id = request.query_params.get("emp_id")
            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            # Validate employee_id
            if not employee_id:
                logger.warning("Missing employee_id parameter")
                return Response(
                    {"message": "Необходимо указать emp_id"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check employee exists
            try:
                employee = Employee.objects.get(id=employee_id)
                logger.debug(f"Found employee: {employee.surname} {employee.name}")
            except Employee.DoesNotExist:
                logger.error(f"Employee not found: {employee_id}")
                return Response(
                    {"message": "Сотрудник не найден"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Handle date range
            today = timezone.now().date()
            
            if start_date_str and end_date_str:
                try:
                    start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                    
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
                # Default to last 30 days
                end_date = today
                start_date = end_date - timedelta(days=30)

            logger.debug(f"Date range for employee {employee_id}: {start_date} to {end_date}")

            # Get reports for employee in date range
            reports = Reports.objects.filter(
                by_employee=employee,
                date__date__gte=start_date,
                date__date__lte=end_date
            ).select_related('function').order_by('date')

            if not reports.exists():
                logger.info(f"No reports found for employee {employee_id}")
                return Response(
                    {
                        "message": "Нет данных за указанный период",
                        "data": {
                            "employee_id": employee.id,
                            "employee_name": f"{employee.surname} {employee.name}",
                            "department_id": employee.department.id,
                            "department_name": employee.department.name,
                            "start_date": start_date,
                            "end_date": end_date,
                            "reports": []
                        }
                    },
                    status=status.HTTP_200_OK
                )

            # Prepare response data
            performance_data = {
                "employee_id": employee.id,
                "employee_name": f"{employee.surname} {employee.name}",
                "department_id": employee.department.id,
                "department_name": employee.department.name,
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
                    "function_id": report.function.id,
                    "function_name": report.function.name,
                    "hours_worked": float(report.hours_worked),
                    "comment": report.comment,
                    "date": date_str
                })

            logger.info(f"Returning performance data for employee {employee_id}")
            return Response(
                {
                    "message": "Данные о производительности сотрудника",
                    "data": performance_data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"Error in EmployeePerformanceView: {str(e)}")
            return Response(
                {"message": "Ошибка при получении данных о производительности"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

