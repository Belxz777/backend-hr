from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

def db_get(objects=[], Serializer=None, curent_class=None):
    send_data = []
    try:
        for obj in objects:
            serializer = Serializer(obj)
            send_data.append(serializer.data)
        return JsonResponse(send_data[0], safe=False) if len(send_data) == 1 else JsonResponse(send_data, safe=False)
    except curent_class.DoesNotExist:
        return JsonResponse({'message': 'The job_title does not exist'}, status=404)

def db_create(request, Serializer=None):
    data = request.data
    serializer = Serializer(data=data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

def db_update(request, Serializer=None, instance=None):
    serializer = Serializer(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=200)
    return JsonResponse(serializer.errors, status=400)

def db_delete(curent_class=None, id=0):
    try:
        obj = curent_class.objects.get(id=id)
        obj.delete()
        return Response({"message": "object deleted successfully"})
    except curent_class.DoesNotExist:
        return Response({"message": "error: object was not deleted"}, status=404)
