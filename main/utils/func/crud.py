import jwt
from django.http import Http404
from main.models import TypicalFunction
from main.serializer import TypicalFunctionSerializer
from main.utils.auth import get_user
from main.utils.closeDate import calculate_close_date
from datetime import datetime
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView

class FunctionView(APIView):
    def get(self, request):
        functions = TypicalFunction.objects.all()
        if not functions:
            return Response({'message': 'No typical functions found'}, status=404)
        serializer = TypicalFunctionSerializer(functions, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = TypicalFunctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(serializer.errors)  # перед return Response(serializer.errors, status=400)
        return Response(serializer.errors, status=400)
        
    def put(self, request, pk):
        function = self.get_object(pk)
        serializer = TypicalFunctionSerializer(function, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        function = self.get_object(pk)
        function.delete()
        return Response(status=204)
        
    def get_object(self, pk):
        try:
            return TypicalFunction.objects.get(pk=pk)
        except TypicalFunction.DoesNotExist:
            raise Http404