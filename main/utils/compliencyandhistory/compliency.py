from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from main.models import Employee,LaborCosts
from main.serializer import LaborCostsSerializer, PerformanceSerializer

class EmployeePerformanceView(APIView):
    def get(self, request):
        # Получаем текущую дату и дату начала последнего месяца
        today = timezone.now().date()
        
        # Получаем employee_id из query parameters
        employee_id = request.query_params.get("emp_id")
        
        # Проверяем, передан ли employee_id
        if not employee_id:
            return Response({"error": "Employee ID (emp_id) is required."}, status=400)
        
        # Получаем объект Employee по employee_id
        try:
            employee = Employee.objects.get(employeeId=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=404)
        
        # Вычисляем дату начала последнего месяца
        last_month_start = today - timedelta(days=30)

        # Фильтруем записи за последний месяц для указанного сотрудника
        labor_costs = LaborCosts.objects.filter(
            employeeId=employee,  # Используем объект Employee
            date__range=[last_month_start, today]
        )

        # Группируем данные по дням и считаем количество отчетов и суммарное количество часов
        performance_data = labor_costs.values('date').annotate(
            report_count=Count('laborCostId'),
            total_hours=Sum('workingHours')
        ).order_by('date')

        # Сериализуем данные с помощью PerformanceSerializer
        serializer = PerformanceSerializer(performance_data, many=True)

        # Возвращаем результат
        return Response({
            "employee_id": employee.employeeId,
            "performance": serializer.data
        })