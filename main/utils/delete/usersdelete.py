from main.models import Employee
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView


def delete_user(request, id):
    user = Employee.objects.filter(employeeId=id).first()
    if user:
        user.delete()
        return Response({'message': 'Сотрудник удален'}, status=204)
    return Response({'error': 'Сотрудник не найден'}, status=404)