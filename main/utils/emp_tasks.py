from rest_framework.views import APIView
from ..models import Job,Department,Task
from rest_framework.decorators import api_view
from ..serializer import JobSerializer,DepartmentSerializer,TaskSerializer,LaborCostsSerializer
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
    def get(self, request,id):
        if id:
            tasks = Task.objects.filter(forEmployeeId=id)    
            return Response(TaskSerializer(tasks, many=True).data)
        else:
            return Response({'error': 'Не указан id'})


