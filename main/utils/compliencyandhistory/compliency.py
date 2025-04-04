# from django.utils import timezone
# from datetime import timedelta
# from django.db.models import Count, Sum
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from main.models import Employee,LaborCosts
# from main.serializer import LaborCostsSerializer, PerformanceSerializer

# class EmployeePerformanceView(APIView):
#     def get(self, request):
#         # Получаем текущую дату и дату начала последнего месяца
#         today = timezone.now().date()
        
#         # Получаем employee_id из query parameters
#         employee_id = request.query_params.get("emp_id")
        
#         # Проверяем, передан ли employee_id
#         if not employee_id:
#             return Response({"error": "Employee ID (emp_id) is required."}, status=400)
        
#         # Получаем объект Employee по employee_id
#         try:
#             employee = Employee.objects.get(employeeId=employee_id)
#         except Employee.DoesNotExist:
#             return Response({"error": "Employee not found."}, status=404)
        
#         # Вычисляем дату начала последнего месяца
#         last_month_start = today - timedelta(days=30)

#         # Фильтруем записи за последний месяц для указанного сотрудника
#         labor_costs = LaborCosts.objects.filter(
#             employeeId=employee,  # Используем объект Employee
#             date__range=[last_month_start, today]  # Добавляем 1 день, чтобы включить текущую дату
#         )

#         # Группируем данные по дням и считаем количество отчетов и суммарное количество часов
#         performance_data = labor_costs.values('date').annotate(
#             report_count=Count('laborCostId'),
#             total_hours=Sum('worked_hours')
#         ).order_by('date')

#         # Сериализуем данные с помощью PerformanceSerializer
#         serializer = PerformanceSerializer(performance_data, many=True)

#         # Возвращаем результат
#         return Response({
#             "employee_id": employee.employeeId,
#             "performance": serializer.data
#         })
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Employee, LaborCosts
from main.serializer import PerformanceSerializer

class EmployeePerformanceView(APIView):
    def get(self, request):
        try:
            # Get current time with timezone
            now = timezone.now()
            today = now.date()
            
            employee_id = request.query_params.get("emp_id")
            
            if not employee_id:
                return Response({"error": "Employee ID (emp_id) is required."}, status=400)
            
            try:
                employee = Employee.objects.get(employeeId=employee_id)
            except Employee.DoesNotExist:
                return Response({"error": "Employee not found."}, status=404)
            
            last_month_start = now - timedelta(days=30)
            
            print(f"Searching records between {last_month_start} and {now}")
            
            # Filter using timezone-aware datetimes
            labor_costs = LaborCosts.objects.filter(
                employeeId=employee.employeeId,  # Use ID or object depending on your model
            ).order_by('date')
            
            print("Raw labor costs:", list(labor_costs.values('laborCostId', 'date')))
            
            if not labor_costs.exists():
                return Response({
                    "employee_id": employee.employeeId,
                    "message": f"No labor records found between {last_month_start.date()} and {today}",
                    "performance": []
                }, status=200)

            # Group by date and collect all records for each date
            performance_by_date = {}
            for cost in labor_costs:
                date_str = cost.date.strftime('%Y-%m-%d')
                if date_str not in performance_by_date:
                    performance_by_date[date_str] = []
                performance_by_date[date_str].append({
                    "laborCostId": cost.laborCostId,
                    "employeeId_id": cost.employeeId_id,
                    "departmentId": cost.departmentId,
                    "tf_id": cost.tf_id,
                    "worked_hours": cost.worked_hours,
                    "normal_hours": cost.normal_hours,

                })

            return Response({
                "employee_id": employee.employeeId,
                "performance": performance_by_date
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
class EmployeeCompliancyView(APIView):
    def get(self, request):
        try:
            # Get current time with timezone
            now = timezone.now()
            today = now.date()
            
            employee_id = request.query_params.get("emp_id")
            
            if not employee_id:
                return Response({"error": "Employee ID (emp_id) is required."}, status=400)
            
            try:
                employee = Employee.objects.get(employeeId=employee_id)
            except Employee.DoesNotExist:
                return Response({"error": "Employee not found."}, status=404)
            
            last_month_start = now - timedelta(days=30)
            
            # Filter using timezone-aware datetimes
            labor_costs = LaborCosts.objects.filter(
                employeeId=employee.employeeId,
            ).values('date').distinct()
            
            if not labor_costs.exists():
                return Response({
                    "employee_id": employee.employeeId,
                    "message": f"No labor records found between {last_month_start.date()} and {today}",
                    "performance": {}
                }, status=200)

            # Create a dict with all days in the last 30 days
            performance_by_date = {}
            current_date = last_month_start.date()
    # Mark only days where employee worked
            performance_by_date = {}
            for record in labor_costs:
                date_str = record['date'].strftime('%Y-%m-%d')
                performance_by_date[date_str] = {"worked": True}

            return Response({
                "employee_id": employee.employeeId,
                "performance": performance_by_date
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)