from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from main.models import Employee, LaborCosts,TypicalFunction
from main.serializer import LaborCostsSerializer
from main.utils.auth import get_user
from main.utils.closeDate import isExpired

@api_view(['POST'])
def labor_fill(request):
    if request.method == 'POST':
        employee = get_user(request)
        if not employee:
            return Response({"error": "Рабочий под таким номером не существует"}, status=404)
        data = request.data
        tf = data.get('tf_id')
        if tf is None:
            return Response({"error": "Не указан tf"}, status=400)
        try:
            tf =TypicalFunction.objects.get(tfId=tf)
        except tf.DoesNotExist:
            return Response({"error": "Задача не найдена"}, status=404)

        # Проверка, принадлежит ли задача сотруднику
        data = request.data
        departmentId = employee.departmentid
        
        if not tf in employee.departmentid.tfs.all():
            return Response({"error": "В вашем отделе нет этой задачи"}, status=403)
       
        laborCost = LaborCosts.objects.create(
            employeeId=employee,
            departmentId=departmentId.departmentId,
            tf = tf,
            worked_hours =data['workingHours'],
            normal_hours = tf.time,
            comment=data['comment']
        )

        if not laborCost:
            return Response({'error': 'Возможно вы отправили неправильные данные | Посмотрите тело запроса.'}, status=400)

        return Response({'message': 'Запись о проделанной работе сделана. Хорошего вам дня!'}, status=201)
        
# @api_view(['POST'])
# def labor_fill(request):
#     if request.method == 'POST':
#         employee = get_user(request)
#         task_id = request.query_params.get("task_id")
#         if not employee:
#             return Response({"error": "Рабочий под таким номером не существует"}, status=404)

#         try:
#             task = Task.objects.get(taskId=task_id)
#         except Task.DoesNotExist:
#             return Response({"error": "Задача не найдена"}, status=404)

#         # Проверка, принадлежит ли задача сотруднику
#         if task.forEmployeeId != employee:
#             return Response({"error": "Вы не можете отправить отчет, так как это не ваша задача"}, status=403)

#         data = request.data
#         departmentId = employee.departmentid.departmentId

#         # Создание записи о трудозатратах
#         laborCost = LaborCosts.objects.create(
#             employeeId=employee,
#             departmentId=departmentId,
#             taskId=task,
#             workingHours=data['workingHours'],
#             comment=data['comment']
#         )

#         if not laborCost:
#             return Response({'error': 'Возможно вы отправили неправильные данные | Посмотрите тело запроса.'}, status=400)

#         # Обновление задачи
#         made = float(task.hourstodo) - float(data['workingHours'])

#         if made <= 0:
#             # Задача завершена
#             task.status = 'completed'
#             task.hourstodo = 0

#             # Обновление счетчиков сотрудника
#             if employee.tasksCount is None:
#                 employee.tasksCount = 0
#             employee.tasksCount -= 1

#             if employee.completedTasks is None:
#                 employee.completedTasks = 0
#             employee.completedTasks += 1

#             # Проверка на истечение срока
#             if isExpired(datetime.now(), task.closeDate):
#                 task.isExpired = True
#                 if employee.expiredTasksCount is None:
#                     employee.expiredTasksCount = 0
#                 employee.expiredTasksCount += 1
#         else:
#             # Задача не завершена
#             task.hourstodo = made
#             if not task.been:
#                 task.been = True

#         # Сохранение изменений
#         task.save()
#         employee.save()

#         return Response({'message': 'Запись о проделанной работе сделана. Хорошего вам дня!'}, status=201)
    
# api_view(['GET'])

# def get_labor_costs(request,id):
#     labor_costs = LaborCosts.objects.filter(departmentId=id)
#     serializer = LaborCostsSerializer(labor_costs, many=True)
#     if serializer.is_valid():
#         return Response(serializer.data)
#     else:
#         return Response({'error':serializer.errors,'possiblefix':"Обратитесь к разработчику программы."}, status=400)
    

@api_view(['DELETE'])
def delete_user(request, id):
    user = Employee.objects.filter(employeeId=id).first()
    if user:
        user.delete()
        return Response({'message': 'Сотрудник удален'}, status=204)
    return Response({'error': 'Сотрудник не найден'}, status=404)