from rest_framework.views import APIView
from rest_framework.decorators import api_view
from main.models import Deputy, Functions, Job
from main.utils.auth import get_user

from rest_framework.response import Response



@api_view(['GET'])
def get_user_functions(request):
    user = get_user(request)
    if user is None:
        return Response({'error': 'Пользователь не авторизован'}, status=401)
    

    job = Job.objects.filter(jobId=user.jobid.jobId).values('jobName', 'deputy').first()
    if job['deputy'] is None:
        deputy = None
        return Response({ 'status':"Обязанностей нет"}, status=200)
    else:
        deputy = Deputy.objects.filter(deputyId=job['deputy'] ).values('deputyId', 'deputyName', 'compulsory').first()
        function = Functions.objects.filter(consistent=deputy['deputyId']).values('funcName')

    non_compulsory_deputies = Deputy.objects.filter(compulsory=False).values('deputyId', 'deputyName')

    return Response({ 'non-compulsory':  non_compulsory_deputies, 'functions': function})