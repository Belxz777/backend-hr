from rest_framework.response import Response
from .models import Job,Department,Project,Task,Employee
from .serializer import JobSerializer,DepartmentSerializer,ProjectSerializer,TaskSerializer,EmployeeSerializer
from rest_framework.views import APIView

from .utils.token_managing import check_token


class  JobManaging(APIView):  
     def patch(self, request,id):
             check_token(request)
             job = Job.objects.filter(jobId=request.data.get('id')).first()
             if job:
                    serializer = JobSerializer(job, data=request.data, partial=True)
                    if serializer.is_valid():
                        job = serializer.save()
                        return Response(JobSerializer(job).data)
                    return Response(serializer.errors, status=400)
             return Response({'error': 'Должность удалена'}, status=404) 
     def delete(self, request,id):
                if id:
                      job = Job.objects.filter(jobId=id)
                if job:
                    job.delete()
                    return Response({'message': 'Должность удалена'}, status=204)
                return Response({'error': 'Jobl not found'}, status=404)       
     def get(self, request, id=None):
                if id:  # If id is provided
                    job = Job.objects.filter(jobId=id).first()
                    if job:
                        serializer = JobSerializer(job)
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Должность не найдена'}, status=404)
                else:
                    jobs = Job.objects.all()
                    serializer = JobSerializer(jobs, many=True)
                    return Response(serializer.data)
                    

class JobList(APIView):

    def post(self, request):
                serializer = JobSerializer(data=request.data)
                if serializer.is_valid():   
                    job = serializer.save()  # Use save() instead of create()
                    return Response(JobSerializer(job).data, status=201)  # Serialize the saved job
                return Response(serializer.errors, status=400)    
    def get(self, request):
        check_token(request)
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    

class DepartmentManaging(APIView):
    def post(self, request):
        # check_token(request)
        serializer =  DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def patch(self, request,id):
             department = Department.objects.filter(departmentId=request.data.get('id')).first()
             if department:
                    serializer = DepartmentSerializer(department, data=request.data, partial=True)
                    if serializer.is_valid():
                        department = serializer.save()
                        return Response(DepartmentSerializer(department).data)
                    return Response(serializer.errors, status=400)
             return Response({'error': ''}, status=404)
    def delete(self, request,id):
                if id:
                      department = Department.objects.filter(departmentId=id)
                if department:
                    department.delete()
                    return Response({'message': 'Отдел удален'}, status=204)
                return Response({'error': 'Отдел не найден'}, status=404)
    def get(self, request, id=None):
                if id:  # If id is provided
                    department = Department.objects.filter(departmentId=id).first()
                    if department:
                        serializer = DepartmentSerializer(department)
                        return Response(serializer.data)
                    else:
                        return Response({'error': 'Отдел не найден'}, status=404)
    
class DepartmentList(APIView):
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    


class ProjectManaging(APIView):
    def post(self, request,id):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    def get(self, request,id):
        projects = Project.objects.filter(projectId=id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    def patch(self, request,id):
             project = Project.objects.filter(projectId=request.data.get('id')).first()
             if project:
                    serializer = ProjectSerializer(project, data=request.data, partial=True)
                    if serializer.is_valid():
                        project = serializer.save()
                        return Response(ProjectSerializer(project).data)
                    return Response(serializer.errors, status=400)
             return Response({'error': ''}, status=404)
    def delete(self, request,id):
                if id:
                      project = Project.objects.filter(projectId=id)
                if project:
                    project.delete()
                    return Response({'message': 'Проект удален'}, status=204)
                return Response({'error': 'Проект не найден'}, status=404)
    
class ProjectByName(APIView):
    def get(self, request, name):
        projects = Project.objects.filter(projectName=name)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    

class UserByName(APIView):
    def get(self, request, name):
        if name:
            users = Employee.objects.filter(userName=name)
            serializer = EmployeeSerializer(users, many=True) 

        # возвращать только фио
            return Response(serializer.data)
        return Response({'error': 'Пользователь не найден'}, status=404)
    
class TaskManaging(APIView):
      def post(self, request,id):
        request.data['byEmployeeId'] = id
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
      def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
      def patch(self, request,id):
             task = Task.objects.filter(taskId=request.data.get('id')).first()
             if task:
                    serializer = TaskSerializer(task, data=request.data, partial=True)
                    if serializer.is_valid():
                        task = serializer.save()
                        return Response(TaskSerializer(task).data)
                    return Response(serializer.errors, status=400)
             return Response({'error': ''}, status=404)
      def delete(self, request,id):
                if id:
                      task = Task.objects.filter(taskId=id)
                if task:
                    task.delete()
                    return Response({'message': 'Задача удалена'}, status=204)
                return Response({'error': 'Задача не найдена'}, status=404)
      




