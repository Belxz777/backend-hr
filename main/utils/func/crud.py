from django.http import Http404
from main.models import Deputy, Functions
from main.serializer import DeputySerializer, FunctionsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class DeputyView(APIView):
    def get(self, request):
        deputies = Deputy.objects.all()
        if not deputies:
            return Response({'message': 'No deputies found'}, status=404)
        serializer = DeputySerializer(deputies, many=True)
        return Response(serializer.data)

    def post(self, request):
        if isinstance(request.data, list):
            responses = []
            for item in request.data:
                serializer = DeputySerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    responses.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            return Response(responses, status=201)
        else:
            serializer = DeputySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

    def patch(self, request):
        deputy = Deputy.objects.get(tfId=request.query_params.get('id'))
        if deputy is None:
            return Response({'message': 'Deputy not found'}, status=404)
        serializer = DeputySerializer(deputy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        deputy = Deputy.objects.get(tfId=request.query_params.get('id'))
        deputy.delete()
        return Response(status=204)

    def get_object(self, pk):
        try:
            return Deputy.objects.get(pk=pk)
        except Deputy.DoesNotExist:
            raise Http404

class FunctionsView(APIView):
    def get(self, request):
        functions = Functions.objects.all()
        if not functions:
            return Response({'message': 'No functions found'}, status=404)
        serializer = FunctionsSerializer(functions, many=True)
        return Response(serializer.data)

    def post(self, request):
        if isinstance(request.data, list):
            responses = []
            for item in request.data:
                serializer = FunctionsSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    responses.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            return Response(responses, status=201)
        else:
            serializer = FunctionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

    def patch(self, request):
        function = Functions.objects.get(funcId=request.query_params.get('id'))
        if function is None:
            return Response({'message': 'Function not found'}, status=404)
        serializer = FunctionsSerializer(function, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        function = Functions.objects.get(funcId=request.query_params.get('id'))
        function.delete()
        return Response(status=204)

    def get_object(self, pk):
        try:
            return Functions.objects.get(pk=pk)
        except Functions.DoesNotExist:
            raise Http404