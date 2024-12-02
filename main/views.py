from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Job,Department
from .serializer import JobSerializer,DepartmentSerializer
from rest_framework.views import APIView
class  JobManaging(APIView):  
     def patch(self, request,id):
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
                    

class JobList(APIView):
    def post(self, request):
                serializer = JobSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    

class DepartmentManaging(APIView):
    def post(self, request):
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