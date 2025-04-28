from datetime import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Employee,Job,Deputy,Functions
from main.utils.auth import get_user


@api_view(['GET'])
def userfuncs(request):
    user = get_user(request)
    if user:
        job = Job.objects.get(jobId=user.jobId)
        deputy = Deputy.objects.get(deputyId = job.deputy)
        nonf = Deputy.objects.get(isExt=True)
        funcs = deputy.deputy_functions.all()
        if funcs.exists():
            return Response({'deputy': deputy, "non-forcable": nonf, "funcs": funcs})
        return Response({'deputy': deputy, "non-forcable": nonf})    
    return Response({"error": "User not found"}, status=401)

def userfuncstoreport(request):
    user = get_user(request)
    if user:
        job = Job.objects.get(jobId=user.jobId)
        deputy = Deputy.objects.get(deputyId = job.deputy)
        nonf = Deputy.objects.get(isExt=True)
        funcs = deputy.deputy_functions.all()
        if funcs.exists():
            return Response({"non-forcable": nonf, "funcs": funcs})
        return Response({'deputy': deputy, "non-forcable": nonf})
    return Response({"error": "User not found"}, status=401)
