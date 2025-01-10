from rest_framework.views import APIView

from main.utils.auth import get_user
from ..models import Task
from ..serializer import TaskSerializer
from rest_framework.response import Response
class EmployeeTasksbystatus(APIView):
    def get(self, request, status,id):
        if id and status:
            print(status)
            tasks = Task.objects.filter(forEmployeeId=id, status=status)    
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id или статус'})
class AllEmployeeTasks(APIView):
    def get(self, request):
        user = get_user(request)
        if user.employeeId:
                    tasks = Task.objects.filter(forEmployeeId=user.employeeId).values('taskName', 'taskDescription', 'status', 'hourstodo', 'closeDate', 'isExpired') 
                    structured_tasks = {}
                    expired_tasks = []  
                    for task in tasks:
                        if task['isExpired']:
                            if task not in expired_tasks:
                                expired_tasks.append(task)
                        else:
                            status = task['status']
                            if status not in structured_tasks:
                                structured_tasks[status] = []
                            structured_tasks[status].append(task)
                    return Response({'all': structured_tasks, 'expired_tasks': expired_tasks}) 
        else: # Changed to return tasks structured by status        else:
            return Response({'error': 'Не указан id'})
class ToReportTasks(APIView):
    def get(self, request):
        user = get_user(request)
        if user.employeeId:
            tasks = Task.objects.filter(forEmployeeId=user.employeeId, status__in=['todo', 'in_progress'])         
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id'})

   