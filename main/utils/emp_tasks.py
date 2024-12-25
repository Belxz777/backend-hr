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
            tasks = Task.objects.filter(forEmployeeId=user.employeeId) 
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id'})


   