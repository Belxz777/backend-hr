from datetime import datetime, timezone
import io
from django.http import HttpResponseBadRequest, HttpResponseForbidden, StreamingHttpResponse
from openpyxl import Workbook
from requests import Response
from rest_framework.decorators import api_view
from openpyxl.utils import get_column_letter
from main.models import Employee,LaborCosts, Task
from main.serializer import LaborCostsSerializer
from main.utils.auth import get_user


@api_view(['GET'])
def get_labor_costs_xlsx(request):
    user = get_user(request)
    
    labor_costs = LaborCosts.objects.filter(departmentId=user.departmentid)
    serializer = LaborCostsSerializer(labor_costs, many=True)
    print(serializer.data)
    for cost in serializer.data:
        task = Task.objects.get(taskId=cost['taskId'])   
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Трудозатраты"

    # Заголовки столбцов
    headers = ['ID_report', 'ID_employee',  'ID_task',"Task_name","Task_from_date" , 'Current_date', 'Worked_h', 'Left_task_h','Comment']
    ws.append(headers)
    column_widths = {i: len(header) for i, header in enumerate(headers, start=1)}


    # Заполняем данными
    for cost in serializer.data:
        row = [
            cost['laborCostId'],
            cost['employeeId'],
            cost['taskId'],
            task.taskName,
            task.fromDate.date(),
            cost['date'],
            cost['workingHours'],
            task.hourstodo,
            cost['comment']
        ]
        ws.append(row)
        for i, value in enumerate(row, start=1):
            column_widths[i] = max(column_widths[i], len(str(value)))

    # Устанавливаем ширину столбцов с небольшим запасом
    for i, width in column_widths.items():
            ws.column_dimensions[get_column_letter(i)].width = width + 2  # Доб
    wb.save(output) 
    output.seek(0)  
    today_date = datetime.now().strftime('%Y-%m-%d')  # Формат YYYY-MM-DD
    filename = f'трудозатраты_{today_date}.xlsx'  # Формируем имя файла

    # Создаем HTTP ответ с содержимым Excel файла
    response = StreamingHttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@api_view(['POST'])
def get_xlsx_precise(request):
            if request.method == 'POST':
                print("Received POST request",request.COOKIES)  
                user = get_user(request)
                data = request.data
                print(data)
                employee_ids = data.get('employee_ids', [])
                from_date = data.get('from_date')
                end_date = data.get('end_date')
                is_boss = user.isBoss
                print(user)
                if not is_boss:
                    print("Access denied for employees.")
                    return HttpResponseForbidden("Access denied for employees.")
        
                labor_costs = LaborCosts.objects.filter(
                    employeeId__in=employee_ids,
                    date__range=[from_date, end_date]
                )
        
                serializer = LaborCostsSerializer(labor_costs, many=True)
                output = io.BytesIO()
                wb = Workbook()
                ws = wb.active
                ws.title = "Трудозатраты"
        
                # Заголовки столбцов
                headers = ['ID_report', 'ID_employee', 'ID_task', "Task_name", "Task_from_date", 'Current_date', 'Worked_h', 'Left_task_h', 'Comment']
                ws.append(headers)
                column_widths = {i: len(header) for i, header in enumerate(headers, start=1)}
        
                # Заполняем данными
                for cost in serializer.data:
                    task = Task.objects.get(taskId=cost['taskId'])
                    row = [
                        cost['laborCostId'],
                        cost['employeeId'],
                        cost['taskId'],
                        task.taskName,
                        task.fromDate.date(),
                        cost['date'],
                        cost['workingHours'],
                        task.hourstodo,
                        cost['comment']
                    ]
                    ws.append(row)
                    for i, value in enumerate(row, start=1):
                        column_widths[i] = max(column_widths[i], len(str(value)))
        
                # Устанавливаем ширину столбцов с небольшим запасом
                for i, width in column_widths.items():
                    ws.column_dimensions[get_column_letter(i)].width = width + 2  # Доб
                wb.save(output)
                output.seek(0)
                today_date = datetime.now().strftime('%Y-%m-%d')  # Формат YYYY-MM-DD
                filename = f'трудозатраты_{today_date}.xlsx'  # Формируем имя файла
        
                # Создаем HTTP ответ с содержимым Excel файла
                response = StreamingHttpResponse(
                    output,
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
                return response
            
            return HttpResponseBadRequest("Invalid request method.")  # Handle GET request case
        
