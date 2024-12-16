from datetime import timezone
from requests import Response
from rest_framework.decorators import api_view

from main.models import Employee,LaborCosts
from main.serializer import LaborCostsSerializer


@api_view(['GET'])
def get_labor_costs(request,id):
    labor_costs = LaborCosts.objects.filter(departmentId=id)
    serializer = LaborCostsSerializer(labor_costs, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)