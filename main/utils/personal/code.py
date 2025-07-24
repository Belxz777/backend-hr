from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Deputy, Functions, Job
from main.utils.auth import get_user
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger("report_functions")

@api_view(['GET'])  # Добавляем декоратор api_view
def get_user_functions(request):
    # Логируем начало выполнения запроса
    logger.info(f"Starting get_user_functions for request: {request.method} {request.path}")
    
    try:
        # Get authenticated user
        user = get_user(request)
        if not user:
            logger.warning(f"Unauthorized access attempt from IP: {request.META.get('REMOTE_ADDR')}")
            return Response(
                {'error': 'Пользователь не авторизован'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        logger.debug(f"Authenticated user: {user.login} (ID: {user.employeeId})")

        try:
            job = Job.objects.get(jobId=user.jobid.jobId)
            logger.debug(f"Found job for user: {job.jobName} (ID: {job.jobId})")
        except ObjectDoesNotExist:
            logger.error(f"Job not found for user {user.login} (ID: {user.employeeId})")
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
                logger.debug(f"Found deputy for job: {deputy.deputyName} (ID: {deputy.deputyId})")
                
                response_data['deputy'] = {
                    'id': deputy.deputyId,
                    'name': deputy.deputyName,
                    'isCompulsory': deputy.compulsory,
                    'functions': list(deputy.deputy_functions.values('funcId', 'funcName'))
                }
            except ObjectDoesNotExist:
                logger.warning(f"Deputy not found for job {job.jobId} though it was referenced")

        # Get all functions
        functions = Functions.objects.all().values('funcId', 'funcName')
        response_data['functions'] = list(functions)
        logger.debug(f"Loaded {len(response_data['functions'])} functions")

        # Get non-compulsory deputies with their functions
        non_compulsory_deputies = Deputy.objects.filter(compulsory=False).prefetch_related('deputy_functions')
        logger.debug(f"Found {non_compulsory_deputies.count()} non-compulsory deputies")
        
        non_compulsory_data = []
        for deputy in non_compulsory_deputies:
            deputy_data = {
                'deputyId': deputy.deputyId,
                'deputyName': deputy.deputyName,
                'functions': list(deputy.deputy_functions.values('funcId', 'funcName'))
            }
            non_compulsory_data.append(deputy_data)
        response_data['nonCompulsory'] = non_compulsory_data

        logger.info(f"Successfully prepared response for user {user.login}")
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.exception(f"Unexpected error in get_user_functions: {str(e)}")
        return Response(
            {'error': 'Произошла внутренняя ошибка сервера'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json'  # Явно указываем content_type
        )