from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Deputy, Functions, Job
from main.utils.auth import get_user
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
@api_view(['GET'])
def get_user_functions(request):
    try:
        # Get authenticated user
        user = get_user(request)
        if not user:
            return Response(
                {'error': 'Пользователь не авторизован'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get user's job
        try:
            job = Job.objects.get(jobId=user.jobid.jobId)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Должность пользователя не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # Prepare response data structure
        response_data = {
            'functions': [],
            'nonCompulsory': []
        }

        # Check if job has deputy assigned
        if hasattr(job, 'deputy') and job.deputy:
            try:
                deputy = Deputy.objects.get(deputyId=job.deputy.deputyId)
                response_data['deputy'] = {
                    'id': deputy.deputyId,
                    'name': deputy.deputyName,
                    'isCompulsory': deputy.compulsory,
                    'functions': list(deputy.deputy_functions.values('funcId', 'funcName'))
                }
            except ObjectDoesNotExist:
                pass

        # Get all functions (using values() for proper serialization)
        functions = Functions.objects.all().values('funcId', 'funcName')  # Adjust fields as needed
        response_data['functions'] = list(functions)

        # Get non-compulsory deputies with their functions
        non_compulsory_deputies = Deputy.objects.filter(compulsory=False).prefetch_related('deputy_functions')
        non_compulsory_data = []
        for deputy in non_compulsory_deputies:
            deputy_data = {
                'deputyId': deputy.deputyId,
                'deputyName': deputy.deputyName,
                'functions': list(deputy.deputy_functions.values('funcId', 'funcName'))
            }
            non_compulsory_data.append(deputy_data)
        response_data['nonCompulsory'] = non_compulsory_data

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Произошла ошибка: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )