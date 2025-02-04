from rest_framework.views import APIView
from rest_framework.decorators import api_view
from main.utils.auth import get_user
from ..models import Employee, Task
from ..serializer import EmployeeSerializer, TaskSerializer
from rest_framework.response import Response
class EmployeeTasksbystatus(APIView):
    def get(self, request, status):
        userid = get_user(request).employeeId
        if userid and status:
            print(status)
            tasks = Task.objects.filter(forEmployeeId=userid, status=status)    
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id или статус'})
class AllEmployeeTasks(APIView):
    def get(self, request):
        user = get_user(request)
        print(user)
        if user.employeeId:
            tasks = Task.objects.filter(forEmployeeId=user.employeeId)
            print(tasks)
            if not tasks: 
                print("no tasks found")
            structured_tasks = {}
            expired_tasks = []  
            for task in tasks:
                if task.isExpired:  # Corrected to access the attribute directly
                    if task not in expired_tasks:   
                        expired_tasks.append(task)
                else:
                    status = task.status  # Corrected to access the attribute directly
                    if status not in structured_tasks:
                        structured_tasks[status] = []     
                    structured_tasks[status].append(TaskSerializer(task).data)  # Serialize task here
            return Response({'all': structured_tasks, 'expired_tasks': TaskSerializer(expired_tasks, many=True).data}) 
        else:            
            return Response({'error': 'Не указан id'}) 
class ToReportTasks(APIView):
    def get(self, request):
        userid = get_user(request).employeeId
        print(userid)
        if userid:
            tasks = Task.objects.filter(forEmployeeId=userid, status__in=['in_progress', 'not_started'])     
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id'}) 
        
@api_view(['GET'])
def getDepEmp(request, id):
    if request.method == 'GET':
        user = get_user(request)
        employees = Employee.objects.filter(departmentid_id=id).exclude(employeeId=user.employeeId)
        return Response(employees.values('employeeId', 'firstName', 'lastName'))    