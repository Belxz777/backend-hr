from rest_framework.views import APIView
from rest_framework.decorators import api_view
from main.utils.auth import get_user
from ..models import Department, Employee, Job, Functions,Deputy
from ..serializer import EmployeeSerializer, FunctionsSerializer
from rest_framework.response import Response
# class EmployeeTasksbystatus(APIView):
#     def get(self, request):
#         status = request.query_params.get('status')
#         userid = get_user(request).employeeId
#         if userid and status:
#             # print(status)
#             if status == "report":
#                             print("csse")
#                             tasks = Task.objects.filter(forEmployeeId=userid, status__in=['in_progress', 'not_started'])     
#                             return Response(TaskSerializer(tasks, many=True).data)
#             tasks = Task.objects.filter(forEmployeeId=userid, status=status)    
#             return Response(TaskSerializer(tasks, many=True).data)
#         else:
#             return Response({'error': 'Не указан id или статус'})
# # class AllEmployeeTasks(APIView):
# #     def get(self, request):
# #         user = get_user(request)
# #         print(user)
# #         if user.employeeId:
# #             tasks = Task.objects.filter(forEmployeeId=user.employeeId)
# #             print(tasks)
# #             if not tasks: 
# #                 print("no tasks found")
# #             structured_tasks = {}
# #             expired_tasks = []  
# #             for task in tasks:
# #                 if task.isExpired:  # Corrected to access the attribute directly
# #                     if task not in expired_tasks:   
# #                         expired_tasks.append(task)
# #                 else:
# #                     status = task.status  # Corrected to access the attribute directly
# #                     if status not in structured_tasks:
# #                         structured_tasks[status] = []     
# #                     structured_tasks[status].append(TaskSerializer(task).data)  # Serialize task here
# #             return Response({'all': structured_tasks, 'expired_tasks': TaskSerializer(expired_tasks, many=True).data}) 
# #         else:            
# #             return Response({'error': 'Не указан id'}) 
 
@api_view(['GET'])
def getDepEmp(request):
    if request.method == 'GET':
        user = get_user(request)
        employees = Employee.objects.filter(departmentid_id=user.departmentid.departmentId).exclude(employeeId=user.employeeId)
    return Response(employees.values('employeeId', 'firstName', 'lastName','position'))    

 

@api_view(['GET'])
def employeeFuncs(request):
    if request.method == 'GET':
        user = get_user(request)
        if not user:
            return Response({'error': 'Не указан id'})
        job  = Job.objects.filter(jobId=user.jobid.jobId).values('mainFunc')

        if not job:
            return Response({'error': 'Не указан id'})
        
        deputy = Deputy.objects.filter(deputyId=job)
        if not deputy:
            return Response({'error': 'Не указан id'})
        
        non_forcable = Deputy.objects.filter(compulsory=False)

        # Get department TFs
     
        # Combine both querysets and remove duplicates
        all_tfs = deputy.union(non_forcable)

        return Response(all_tfs)
    
@api_view(['GET'])
def departmentTf(request):
    if request.method == 'GET':
        id = request.query_params.get('id')
        tfs = Department.objects.filter(departmentId=id).values('tfs')
        type = Functions.objects.filter(funcId__in=tfs).values('funcId', 'funcName','consistent','time')
        return Response(type)


@api_view(['GET'])
def jobTf(request):
    if request.method == 'GET':
        id = request.query_params.get('id')
        tfs = Job.objects.filter(jobId=id).values('tfs')
        type = Functions.objects.filter(funcId__in=tfs).values('funcId', 'funcName','consistent','time')
        return Response(type)