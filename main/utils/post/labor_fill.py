from datetime import timezone
from requests import Response
from rest_framework.decorators import api_view

from main.models import Employee,LaborCosts
from main.serializer import LaborCostsSerializer

@api_view([ 'POST'])
def labor_fill(request,id):
    if request.method == 'POST':
        data = request.data
        employee = Employee.objects.filter(employeeId=id).first()
        departmentId = employee.departmentid
        date = timezone.now()  # Current date and time in Samara timezone
    #         laborCostId = models.IntegerField(primary_key=True)  # Уникальный идентификатор трудозатрат
    # employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    # departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    # taskId = models.ForeignKey(Task, on_delete=models.CASCADE,null=False) # Идентификатор задачии
    # projectId = models.ForeignKey(Project, on_delete=models.CASCADE,null=False) # Идентификатор проектаа
    # date = models.DateField(null=False)  # Дата отчета о работе
    # workingHours = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # Затраченное время
    # comment = models.CharField(max_length=30, null=True)  # Комментарий
    # serviceDescription = models.CharField(max_length=30, null=True)  
        if employee:
            laborCost =LaborCosts.objects.create(
                employeeId=employee,
                departmentId=departmentId,
                taskId=data['taskId'],
                projectId=data['projectId'],
                date= date,
                workingHours=data['workingHours'],
                comment=data['comment'],
                serviceDescription=data['serviceDescription']
            )
            if laborCost:
                return Response({'message': 'Labor cost created successfully'}, status=201)
            else:
                return Response({'error': 'Labor cost not created'}, status=400)
        else:
            return Response({'error': 'Employee not found,imposible to add report'}, status=404)

api_view(['GET'])
def get_labor_costs(request,id):
    labor_costs = LaborCosts.objects.filter(departmentId=id)
    serializer = LaborCostsSerializer(labor_costs, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)