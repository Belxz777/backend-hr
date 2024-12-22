from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Employee,LaborCosts,Task
from main.serializer import LaborCostsSerializer

@api_view([ 'POST'])
def labor_fill(request,id):
    if request.method == 'POST':
        data = request.data
        employee = Employee.objects.filter(employeeId=id).first()
        departmentId = employee.departmentid.departmentId# Current date and time in Samara timezone
        if employee:
    #           laborCostId = models.IntegerField(primary_key=True)  # Уникальный идентификатор трудозатрат
    # employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    # departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    # taskId = models.ForeignKey(Task, on_delete=models.CASCADE,null=False) # Идентификатор задачии
    # date = models.DateField(auto_now_add=True)  # Дата отчета о работе
    # workingHours = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # Затраченное время
    # comment = models.CharField(max_length=30, null=True)
            laborCost = LaborCosts.objects.create(
                employeeId=employee,
                departmentId=departmentId,
                taskId=Task.objects.get(taskId=data['taskId']),  # Ensure taskId is a Task instance
                workingHours=data['workingHours'],
                comment=data['comment']
            )        
            if laborCost:
                task = Task.objects.get(taskId=data['taskId'])
                made = task.hourstodo - data['workingHours']
                print(made)
                if task:
                    if made == 0:
                        task.status = 'completed'
                        task.hourstodo = made
                        task.save()
                    else:
                        if task.been==False:
                            task.been = True
                            task.save()
                        task.hourstodo = made
                        task.save()
                return Response({'message': 'Запись о проделаной работе сделана. / Хорошего вам дня!'}, status=201)
            else:
                return Response({'error': 'Возможно вы отправили не правильные данные | Посмотрите тело запроса.'}, status=400)
        else:
            return Response({'error': 'Рабочий под таким номером не существует '}, status=404)

api_view(['GET'])
def get_labor_costs(request,id):
    labor_costs = LaborCosts.objects.filter(departmentId=id)
    serializer = LaborCostsSerializer(labor_costs, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)