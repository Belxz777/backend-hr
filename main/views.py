
from main.utils.auth import get_user
from .models import Job,Department,Employee
from .serializer import JobSerializer,DepartmentSerializer,EmployeeSerializer
from .utils.access_managing import check_token
import logging
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from .models import Job, Department, Employee


logger = logging.getLogger(__name__)

class JobManaging(APIView):
    def patch(self, request):
        logger.info(f"PATCH request for JobManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            check_token(request)
            id = request.query_params.get('id')
            if not id:
                logger.warning("Missing id parameter in PATCH request")
                return Response({'error': 'ID должности обязателен'}, status=400)
                
            job = get_object_or_404(Job, jobId=id)
            serializer = JobSerializer(job, data=request.data, partial=True)
            
            if serializer.is_valid():
                job = serializer.save()
                logger.info(f"Job {id} updated successfully")
                return Response({'new': JobSerializer(job).data}, status=200)
                
            logger.warning(f"Validation errors in PATCH request: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            logger.exception(f"Error in JobManaging PATCH: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)

    def delete(self, request):
        logger.info(f"DELETE request for JobManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            id = request.query_params.get('id')
            if not id:
                logger.warning("Missing id parameter in DELETE request")
                return Response({'error': 'ID должности обязателен'}, status=400)
                
            job = get_object_or_404(Job, jobId=id)
            job.delete()
            logger.info(f"Job {id} deleted successfully")
            return Response({'message': 'Должность удалена'}, status=204)
            
        except Exception as e:
            logger.exception(f"Error in JobManaging DELETE: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)

    def get(self, request):
        logger.info(f"GET request for JobManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            id = request.query_params.get('id')
            if id:
                job = get_object_or_404(Job, jobId=id)
                serializer = JobSerializer(job)
                return Response(serializer.data)
            else:
                jobs = Job.objects.all()
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in JobManaging GET: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)


class JobList(APIView):
    def post(self, request):
        logger.info(f"POST request for JobList from {request.META.get('REMOTE_ADDR')}")
        try:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                job = serializer.save()
                logger.info(f"New job created with ID: {job.jobId}")
                return Response(JobSerializer(job).data, status=201)
                
            logger.warning(f"Validation errors in Job creation: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            logger.exception(f"Error in JobList POST: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)

    def get(self, request):
        logger.info(f"GET request for JobList from {request.META.get('REMOTE_ADDR')}")
        try:
            check_token(request)
            jobs = Job.objects.all()
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in JobList GET: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)


class DepartmentManaging(APIView):
    def patch(self, request):
        logger.info(f"PATCH request for DepartmentManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            department_id = request.query_params.get('id')
            user = get_user(request)
            
            if not user or user.position != 5:
                logger.warning(f"Unauthorized PATCH attempt by user {user.employeeId if user else 'anonymous'}")
                return Response({'error': 'У вас нет прав на это действие'}, status=403)
            
            if not department_id:
                logger.warning("Missing department ID in PATCH request")
                return Response({"error": "ID обязателен"}, status=400)
            
            department = get_object_or_404(Department, departmentId=department_id)
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            
            if serializer.is_valid():
                department = serializer.save()
                logger.info(f"Department {department_id} updated successfully")
                return Response(DepartmentSerializer(department).data)
                
            logger.warning(f"Validation errors in department update: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            logger.exception(f"Error in DepartmentManaging PATCH: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)

    def delete(self, request):
        logger.info(f"DELETE request for DepartmentManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            department_id = request.query_params.get('id')
            user = get_user(request)
            
            if not user or user.position != 5:
                logger.warning(f"Unauthorized DELETE attempt by user {user.employeeId if user else 'anonymous'}")
                return Response({'error': 'У вас нет прав на это действие'}, status=403)
                
            department = get_object_or_404(Department, departmentId=department_id)
            department.delete()
            logger.info(f"Department {department_id} deleted successfully")
            return Response({'message': 'Отдел удален'}, status=204)
            
        except Exception as e:
            logger.exception(f"Error in DepartmentManaging DELETE: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)

    def get(self, request):
        logger.info(f"GET request for DepartmentManaging from {request.META.get('REMOTE_ADDR')}")
        try:
            department_id = request.query_params.get('id')
            if department_id:
                department = get_object_or_404(Department, departmentId=department_id)
                serializer = DepartmentSerializer(department)
                return Response(serializer.data)
            else:
                logger.warning("Missing department ID in GET request")
                return Response({'error': 'ID отдела обязателен'}, status=400)
        except Exception as e:
            logger.exception(f"Error in DepartmentManaging GET: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)


class DepartmentList(APIView):
    def post(self, request):
        logger.info(f"POST request for DepartmentList from {request.META.get('REMOTE_ADDR')}")
        try:
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                department = serializer.save()
                logger.info(f"New department created with ID: {department.departmentId}")
                return Response(serializer.data, status=201)
                
            logger.warning(f"Validation errors in department creation: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            logger.exception(f"Error in DepartmentList POST: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)


class DepartmentEmployees(APIView):
    def get(self, request, id):
        logger.info(f"GET request for DepartmentEmployees from {request.META.get('REMOTE_ADDR')}")
        try:
            token = request.COOKIES.get('jwt')
            if not token:
                logger.warning("Unauthenticated access attempt to DepartmentEmployees")
                raise AuthenticationFailed({'message': 'Вы не аутентифицированы'})
                
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                logger.warning("Expired JWT token")
                raise AuthenticationFailed('Токен истек')
            except jwt.InvalidTokenError:
                logger.warning("Invalid JWT token")
                raise AuthenticationFailed('Недействительный токен')
                
            user = get_object_or_404(Employee, employeeId=payload['user'])
            department = get_object_or_404(Department, departmentId=id)
            
            if user.departmentid.departmentId != department.departmentId:
                logger.warning(f"User {user.employeeId} tried to access department {id} they don't belong to")
                return Response({'message': 'Вы не можете получить список сотрудников этого отдела'}, status=403)
                
            employees = Employee.objects.filter(departmentid=id).exclude(employeeId=user.employeeId)
            serializer = EmployeeSerializer(employees, many=True)
            logger.info(f"Successfully returned employees for department {id}")
            return Response(serializer.data)
            
        except Exception as e:
            logger.exception(f"Error in DepartmentEmployees GET: {str(e)}")
            return Response({'error': 'Внутренняя ошибка сервера'}, status=500)
  