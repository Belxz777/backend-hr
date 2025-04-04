from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Department, Employee,LaborCosts
from main.serializer import LaborCostsSerializer, PerformanceSerializer

class DepartmentPerformanceView(APIView):
    def get(self, request):
        # Получаем текущую дату и дату начала последнего месяца
        today = timezone.now().date()
        
        # Получаем employee_id из query parameters
        department_id = request.query_params.get("department_id")
        
        # Проверяем, передан ли employee_id
        if not department_id:
            return Response({"error": "Employee ID (emp_id) is required."}, status=400)
        
        # Получаем объект Employee по employee_id
        try:
            department = Department.objects.get(departmentId=department_id)
        except Department.DoesNotExist:
            return Response({"error": "Department not found."}, status=404)
        
        # Вычисляем дату начала последнего месяца
        last_month_start = today - timedelta(days=30)

        # Фильтруем записи за последний месяц для указанного сотрудника
            
        print(f"Searching records between {last_month_start} and {today}")
            
            # Filter using timezone-aware datetimes
        labor_costs = LaborCosts.objects.filter(
                departmentId = department_id,  # Use ID or object depending on your model
            ).order_by('date')
            
        print("Raw labor costs:", list(labor_costs.values('laborCostId', 'date')))
            
        if not labor_costs.exists():
                return Response({
                    "dep_id":department_id,
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
                "dep_id":department_id ,
                "performance": performance_by_date
            })