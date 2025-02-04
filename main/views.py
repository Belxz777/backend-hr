
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt

from main.utils.closeDate import calculate_close_date
from .models import Job,Department,Task,Employee
from .serializer import JobSerializer,DepartmentSerializer,TaskSerializer,EmployeeSerializer
from rest_framework.views import APIView

from .utils.access_managing import check_token


class  JobManaging(APIView):  
     def patch(self, request,id):
             check_token(request)
             job = Job.objects.filter(jobId=request.data.get('id')).first()
             if job:
                    serializer = JobSerializer(job, data=request.data, partial=True)
                    if serializer.is_valid():
                        job = serializer.save()
                        return Response({'newversion':JobSerializer(job).data,},status=200)
                    return Response(serializer.errors, status=400)
             return Response({'error': 'Ошибка'}, status=404) 
     def delete(self, request,id):
                if id:
                      job = Job.objects.filter(jobId=id)
                      if job:
                        job.delete()
                        return Response({'message': 'Должность удалена'}, status=204)
                return Response({'error': 'Такая должность не найдена или не предоставлен id'}, status=404)       
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
    def patch(self, request):
        # Получаем id из query parameters
        department_id = request.query_params.get('id')
        
        if not department_id:
            return Response({"error": "ID is required"}, status=400)
        
        # Ищем отдел по ID
        department = Department.objects.filter(departmentId=department_id).first()
        
        if not department:
            return Response({"error": "Department not found"}, status=404)
        
        # Обновляем отдел
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        
        if serializer.is_valid():
            department = serializer.save()
            return Response(DepartmentSerializer(department).data)
        
        return Response(serializer.errors, status=400)
       
    def delete(self, request):   
                id = request.query_params.get('id')
                department = Department.objects.filter(departmentId=id)
                if department:
                    department.delete()
                    return Response({'message': 'Отдел удален'}, status=204)
                return Response({'error': 'Отдел не найден'}, status=404)
    def get(self, request, id=None):
                    id = request.query_params.get('id')
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
    
class DepartmentEmployees(APIView):
    def get(self, request,id):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed({'message': 'Ты не аутетифицирован '})
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен истек')
        user = Employee.objects.get(employeeId=payload['user'])
        if not user:
            raise AuthenticationFailed('Пользователь не найден')
        department = Department.objects.get(departmentId=id)
        serializer = EmployeeSerializer(user)
        print(user.employeeId,department.departmentId)
        #если пользователь является сотрудником этого отдела, то он может получить список сотрудников этого отдела
        if user.employeeId == department.departmentId:
            employees = Employee.objects.filter(departmentid=id)
            employees = Employee.objects.filter(departmentid=id).exclude(employeeId=user.employeeId)
            serializer = EmployeeSerializer(employees, many=True)      
            return Response(serializer.data)        
        return Response({'message': 'Вы не можете получить список  сотрудников этого отдела'}, status=403)


# class ProjectManaging(APIView):
#     def post(self, request,id):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
#     def get(self, request,id):
#         projects = Project.objects.filter(projectId=id)
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
#     def patch(self, request,id):
#              project = Project.objects.filter(projectId=request.data.get('id')).first()
#              if project:
#                     serializer = ProjectSerializer(project, data=request.data, partial=True)
#                     if serializer.is_valid():
#                         project = serializer.save()
#                         return Response(ProjectSerializer(project).data)
#                     return Response(serializer.errors, status=400)
#              return Response({'error': ''}, status=404)
#     def delete(self, request,id):
#                 if id:
#                       project = Project.objects.filter(projectId=id)
#                 if project:
#                     project.delete()
#                     return Response({'message': 'Проект удален'}, status=204)
#                 return Response({'error': 'Проект не найден'}, status=404)
    
# class ProjectByName(APIView):
#     def get(self, request, name):
#         projects = Project.objects.filter(projectName=name)
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)
    

class UserByName(APIView):
    def get(self, request, name):
        if name:
            users = Employee.objects.filter(userName=name)
            serializer = EmployeeSerializer(users, many=True) 

        # возвращать только фио
            return Response(serializer.data)
        return Response({'error': 'Пользователь не найден'}, status=404)
    
class TaskManaging(APIView):
#http://127.0.0.1:8000/api/v1/entities/task/ enpoint post | patch | delete
      def post(self, request):
#         post | body{
# "forEmployeeId":2,
# "hourstodo":7,
# "taskName":"Реализовать возможность загрузки задачи"
#         }
        request.data['forEmployeeId']
        request.data['closeDate'] = calculate_close_date(request.data['hourstodo'],datetime.now())
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                 'message': 'Задача создана',
                    'taskId': serializer.data['taskId']
            }, status=201)
        return Response({
             'error': 'Не удалось создать задачу',
             'detail': serializer.errors
        }, status=400)
      def patch(self, request):
#    patch |  body{
#     "taskId":12,
#     "taskName":"hello",
# forEmployeeId:1,
# }
             task = Task.objects.filter(taskId=request.data['taskId']).first()
             if task:
                    serializer = TaskSerializer(task, data=request.data, partial=True)
                    if serializer.is_valid():
                        task = serializer.save()
                        return Response({
                             'message': 'Задача обновлена',
                             'params': serializer.data.values()
                        }, status=201)
                    return Response({
                         'error': 'Не удалось обновить задачу',
                         'detail': serializer.errors
                    }, status=400)
             return Response({'error': 'Ошибка задача не найдена'}, status=404)
      def delete(self, request):
                # delete | body {
                #      "taskId":12,
                # }
                task = Task.objects.filter(taskId=request.data['taskId']).first()
                if task:
                    task.delete()
                    return Response({'message': 'Задача удалена',"taskId":request.data['taskId']}, status=204)
                return Response({'error': 'Задача не найдена'}, status=404)
      




