# jobs.py компонент для работы с должностями

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

import logging

from main.models import Job
from main.serializer import JobSerializer

logger = logging.getLogger(__name__)

class JobManaging(APIView):
    def patch(self, request):
        logger.info(f"Job update request from {request.META.get('REMOTE_ADDR')}")
        try:
            id = request.query_params.get('id')
            if not id:
                logger.warning("Missing job ID in request")
                return Response(
                    {'message': 'ID должности обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            job = get_object_or_404(Job, id=id)
            serializer = JobSerializer(job, data=request.data, partial=True)
            
            if not serializer.is_valid():
                logger.warning(f"Validation errors: {serializer.errors}")
                return Response(
                    {
                        'message': 'Ошибки валидации',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            job = serializer.save()
            logger.info(f"Job {id} updated successfully")
            return Response(
                {
                    'message': 'Должность успешно обновлена',
                    'data': JobSerializer(job).data
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.exception(f"Job update error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        logger.info(f"Job deletion request from {request.META.get('REMOTE_ADDR')}")
        try:
            id = request.query_params.get('id')
            if not id:
                logger.warning("Missing job ID in request")
                return Response(
                    {'message': 'ID должности обязателен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            job = get_object_or_404(Job, id=id)
            job.delete()
            logger.info(f"Job {id} deleted successfully")
            return Response(
                {'message': 'Должность успешно удалена'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Exception as e:
            logger.exception(f"Job deletion error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        logger.info(f"Job retrieval request from {request.META.get('REMOTE_ADDR')}")
        try:
            id = request.query_params.get('id')
            if id:
                job = get_object_or_404(Job, id=id)
                serializer = JobSerializer(job)
                return Response(
                    {
                        'message': 'Данные должности',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                jobs = Job.objects.all()
                serializer = JobSerializer(jobs, many=True)
                return Response(
                    {
                        'message': 'Список должностей',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.exception(f"Job retrieval error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JobCreate(APIView):
    def post(self, request):
        logger.info(f"Job creation request from {request.META.get('REMOTE_ADDR')}")
        try:
            serializer = JobSerializer(data=request.data)
            
            if not serializer.is_valid():
                logger.warning(f"Validation errors: {serializer.errors}")
                return Response(
                    {
                        'message': 'Ошибки валидации',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            job = serializer.save()
            logger.info(f"New job created with ID: {job.id}")
            return Response(
                {
                    'message': 'Должность успешно создана',
                    'data': JobSerializer(job).data
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            logger.exception(f"Job creation error: {str(e)}")
            return Response(
                {'message': 'Внутренняя ошибка сервера'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )