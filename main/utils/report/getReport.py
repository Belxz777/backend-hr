from datetime import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view

from main.models import Employee,LaborCosts
from main.serializer import LaborCostsSerializer


@api_view(['GET'])
def get_labor_costs(request):
    id = request.query_params.get("department_id")  
    labor_costs = LaborCosts.objects.filter(departmentId=id)
    serializer = LaborCostsSerializer(labor_costs, many=True)
    return Response(serializer.data)    