import logging
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from main.models import Deputy, Functions
from main.serializer import DeputySerializer, FunctionsSerializer

logger = logging.getLogger(__name__)

class DeputyView(APIView):
    def get(self, request):
        logger.info(f"DeputyView GET request from {request.META.get('REMOTE_ADDR')}")
        try:
            only_compulsory = request.query_params.get('only_compulsory', 'false').lower()
            
            deputies = Deputy.objects.prefetch_related('deputy_functions')
            
            if only_compulsory == 'true':
                deputies = deputies.filter(compulsory=True)
                logger.debug("Filtering only compulsory deputies")
            
            if not deputies.exists():
                logger.warning("No deputies found in database")
                return Response({'message': 'No deputies found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = DeputySerializer(deputies, many=True)
            logger.info(f"Returning {len(serializer.data)} deputies")
            return Response(serializer.data)
            
        except Exception as e:
            logger.exception(f"Error in DeputyView GET: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        logger.info(f"DeputyView POST request from {request.META.get('REMOTE_ADDR')}")
        try:
            if isinstance(request.data, list):
                responses = []
                for item in request.data:
                    serializer = DeputySerializer(data=item)
                    if serializer.is_valid():
                        deputy = serializer.save()
                        logger.info(f"Created deputy with ID: {deputy.deputyId}")
                        responses.append(serializer.data)
                    else:
                        logger.warning(f"Validation errors in bulk create: {serializer.errors}")
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response(responses, status=status.HTTP_201_CREATED)
            else:
                serializer = DeputySerializer(data=request.data)
                if serializer.is_valid():
                    deputy = serializer.save()
                    logger.info(f"Created deputy with ID: {deputy.deputyId}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logger.warning(f"Validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.exception(f"Error in DeputyView POST: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        logger.info(f"DeputyView PATCH request from {request.META.get('REMOTE_ADDR')}")
        try:
            deputy_id = request.query_params.get('id')
            if not deputy_id:
                logger.warning("Missing deputy ID in PATCH request")
                return Response(
                    {'message': 'Deputy ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            deputy = self.get_object(deputy_id)
            serializer = DeputySerializer(deputy, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_deputy = serializer.save()
                logger.info(f"Updated deputy with ID: {updated_deputy.deputyId}")
                return Response(serializer.data)
                
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Http404:
            logger.warning(f"Deputy not found with ID: {deputy_id}")
            return Response(
                {'message': 'Deputy not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error in DeputyView PATCH: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        logger.info(f"DeputyView DELETE request from {request.META.get('REMOTE_ADDR')}")
        try:
            deputy_id = request.query_params.get('id')
            if not deputy_id:
                logger.warning("Missing deputy ID in DELETE request")
                return Response(
                    {'message': 'Deputy ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            deputy = self.get_object(deputy_id)
            deputy.delete()
            logger.info(f"Deleted deputy with ID: {deputy_id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Http404:
            logger.warning(f"Deputy not found with ID: {deputy_id}")
            return Response(
                {'message': 'Deputy not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error in DeputyView DELETE: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_object(self, pk):
        try:
            return Deputy.objects.get(pk=pk)
        except Deputy.DoesNotExist:
            logger.warning(f"Deputy not found with ID: {pk}")
            raise Http404


class FunctionsView(APIView):
    def get(self, request):
        logger.info(f"FunctionsView GET request from {request.META.get('REMOTE_ADDR')}")
        try:
            functions = Functions.objects.all()
            
            if not functions.exists():
                logger.warning("No functions found in database")
                return Response(
                    {'message': 'No functions found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = FunctionsSerializer(functions, many=True)
            logger.info(f"Returning {len(serializer.data)} functions")
            return Response(serializer.data)
            
        except Exception as e:
            logger.exception(f"Error in FunctionsView GET: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        logger.info(f"FunctionsView POST request from {request.META.get('REMOTE_ADDR')}")
        try:
            data = request.data
            serializer = FunctionsSerializer(data=data)
            
            if serializer.is_valid():
                function = serializer.save()
                logger.info(f"Created function with ID: {function.funcId}")
                
                deputy_id = data.get('consistent')
                if deputy_id:
                    try:
                        deputy = Deputy.objects.get(deputyId=deputy_id)
                        deputy.deputy_functions.add(function)
                        deputy.save()
                        logger.info(f"Added function {function.funcId} to deputy {deputy_id}")
                    except Deputy.DoesNotExist:
                        logger.warning(f"Deputy not found with ID: {deputy_id}")
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.exception(f"Error in FunctionsView POST: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        logger.info(f"FunctionsView PATCH request from {request.META.get('REMOTE_ADDR')}")
        try:
            function_id = request.query_params.get('id')
            if not function_id:
                logger.warning("Missing function ID in PATCH request")
                return Response(
                    {'message': 'Function ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            function = self.get_object(function_id)
            serializer = FunctionsSerializer(function, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_function = serializer.save()
                logger.info(f"Updated function with ID: {updated_function.funcId}")
                return Response(serializer.data)
                
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Http404:
            logger.warning(f"Function not found with ID: {function_id}")
            return Response(
                {'message': 'Function not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error in FunctionsView PATCH: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        logger.info(f"FunctionsView DELETE request from {request.META.get('REMOTE_ADDR')}")
        try:
            function_id = request.query_params.get('id')
            if not function_id:
                logger.warning("Missing function ID in DELETE request")
                return Response(
                    {'message': 'Function ID is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            function = self.get_object(function_id)
            function_name = function.funcName
            function_id = function.funcId
            function.delete()
            
            logger.info(f"Deleted function: {function_name} (ID: {function_id})")
            return Response(
                {
                    'message': 'Функция удалена',
                    'name': function_name,
                    'id': function_id
                }, 
                status=status.HTTP_200_OK
            )
            
        except Http404:
            logger.warning(f"Function not found with ID: {function_id}")
            return Response(
                {'message': 'Function not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception(f"Error in FunctionsView DELETE: {str(e)}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_object(self, pk):
        try:
            return Functions.objects.get(pk=pk)
        except Functions.DoesNotExist:
            logger.warning(f"Function not found with ID: {pk}")
            raise Http404