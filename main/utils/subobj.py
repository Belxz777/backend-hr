from rest_framework.views import APIView
from ..models import Job,Department,Project,Task
from ..serializer import JobSerializer,DepartmentSerializer,ProjectSerializer,TaskSerializer,LaborCostsSerializer
from rest_framework.response import Response
class ProjectTasks(APIView):
    def get(self, request, status,id):
        if(id):
            tasks = Task.objects.filter(byEmployeeId=id,status=status)
            if status:
                tasks = Task.objects.filter(tasks,status=status)
            return Response(TaskSerializer(tasks, many=True).data)

