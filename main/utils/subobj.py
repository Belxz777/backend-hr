from rest_framework.views import APIView
from ...models import Job,Department,Project,Task
from .rest_framework.decorators import api_view
from ..serializer import JobSerializer,DepartmentSerializer,ProjectSerializer,TaskSerializer,LaborCostsSerializer
from rest_framework.response import Response
class ProjectTasks(APIView):
    def get(self, request, status,id):
        if id and status:
            tasks = Task.objects.filter(byEmployeeId=id, status=status)    
            return Response(TaskSerializer(tasks, many=True).data)
        

@api_view(['GET'])
def allprojectTasks(request, id):
    if request.method == 'GET':
        # Получаем проект по его ID
        tasks = Task.objects.filter(projectId=id)
        if tasks:
            # Возвращаем данные о проекте и задачах в формате JSON
            return Response({'tasks': TaskSerializer(tasks, many=True).data})
        else:
            return Response({'info': 'Задач не найдено'}, status=404)