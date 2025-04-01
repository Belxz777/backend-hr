# from datetime import datetime, timezone
# import io
# from django.http import HttpResponseBadRequest, HttpResponseForbidden, StreamingHttpResponse
# from openpyxl import Workbook
# from requests import Response
# from rest_framework.decorators import api_view
# from openpyxl.utils import get_column_letter
# from main.models import Employee,LaborCosts, Task
# from main.serializer import LaborCostsSerializer
# from main.utils.auth import get_user


# @api_view(['GET'])
# def get_labor_costs_xlsx(request):
#     user = get_user(request)
    
#     labor_costs = LaborCosts.objects.filter(departmentId=user.departmentid.departmentId)
#     serializer = LaborCostsSerializer(labor_costs, many=True)
    
#     output = io.BytesIO()
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Трудозатраты"

#     # Заголовки столбцов
#     headers = ['report_id', 'employee_id', 'task_id', "task_name", "task_from_date", 'report_date', 'worked_hours', 'left_hours', 'comment']
#     ws.append(headers)
#     column_widths = {i: len(header) for i, header in enumerate(headers, start=1)}

#     # Заполняем данными
#     for cost in serializer.data:
#         task = Task.objects.get(taskId=cost['taskId'])
#         row = [
#             cost['laborCostId'],
#             cost['employeeId'],
#             cost['taskId'],
#             task.taskName,
#             task.fromDate.date(),
#             cost['date'],
#             cost['workingHours'],
#             None if task.hourstodo == 0 else task.hourstodo,
#             cost['comment']
#         ]
#         ws.append(row)
#         for i, value in enumerate(row, start=1):
#             column_widths[i] = max(column_widths[i], len(str(value)))

#     # Устанавливаем ширину столбцов с небольшим запасом
#     for i, width in column_widths.items():
#         ws.column_dimensions[get_column_letter(i)].width = width + 2  # Доб

#     wb.save(output) 
#     output.seek(0)  
#     today_date = datetime.now().strftime('%Y-%m-%d')
#     filename = f'obshii_otchet_{today_date}.xlsx'

#     # Создаем ответ с файлом
#     response = StreamingHttpResponse(
#         output,
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response   # Создаем HTTP ответ с содержимым Excel файла

# @api_view(['POST'])
# def get_xlsx_precise(request):
#     if request.method == 'POST':
#         print("Received POST request", request.COOKIES)
#         user = get_user(request)
#         data = request.data
#         print(data)

#         # Extract employee_ids, start_date, and end_date
#         employee_ids = data.get('employee_ids', [])
#         from_date = data.get('start_date')
#         end_date = data.get('end_date')

#         # Validate input
#         if not employee_ids or not from_date or not end_date:
#             return HttpResponseBadRequest("Missing required parameters: employee_ids, start_date, or end_date.")

#         # Filter labor costs
#         labor_costs = LaborCosts.objects.filter(
#             employeeId__in=employee_ids,
#             date__range=[from_date, end_date]
#         )

#         # If no labor costs found, return an empty Excel file with a message
#         if not labor_costs.exists():
#             output = io.BytesIO()
#             wb = Workbook()
#             ws = wb.active
#             ws.title = "Трудозатраты"
#             ws.append(["No labor costs found for the given criteria."])
#             wb.save(output)
#             output.seek(0)

#             filename = f'persise_{datetime.now().strftime("%Y-%m-%d")}.xlsx'
#             response = StreamingHttpResponse(
#                 output,
#                 content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#             )
#             response['Content-Disposition'] = f'attachment; filename="{filename}"'
#             return response

#         # Serialize labor costs
#         serializer = LaborCostsSerializer(labor_costs, many=True)

#         # Create Excel file
#         output = io.BytesIO()
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Трудозатраты"

#         # Define headers
#         headers = ['report_id', 'employee_id', 'task_id', "task_name", "task_from_date", 'report_date', 'worked_hours', 'left_hours', 'comment']
#         ws.append(headers)
#         column_widths = {i: len(header) for i, header in enumerate(headers, start=1)}

#         # Populate data
#         for cost in serializer.data:
#             task = Task.objects.get(taskId=cost['taskId'])
#             row = [
#                 cost['laborCostId'],
#                 cost['employeeId'],
#                 cost['taskId'],
#                 task.taskName,
#                 task.fromDate.date(),
#                 cost['date'],
#                 cost['workingHours'],
#                 None if task.hourstodo == 0 else task.hourstodo,
#                 cost['comment']
#             ]
#             ws.append(row)
#             for i, value in enumerate(row, start=1):
#                 column_widths[i] = max(column_widths[i], len(str(value)))

#         # Set column widths
#         for i, width in column_widths.items():
#             ws.column_dimensions[get_column_letter(i)].width = width + 2

#         # Save workbook to output buffer
#         wb.save(output)
#         output.seek(0)

#         # Generate filename with current date
#         today_date = datetime.now().strftime('%Y-%m-%d')
#         filename = f'tochnii_otchet_{today_date}.xlsx'

#         # Create HTTP response
#         response = StreamingHttpResponse(
#             output,
#             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#         )
#         response['Content-Disposition'] = f'attachment; filename="{filename}"'

#         return response

#     return HttpResponseBadRequest("Invalid request method. Only POST requests are allowed.")

# @api_view(['GET'])
# def get_all_labor_costs_xlsx(request):
#     # Check for security code in params
#     code = request.GET.get('code')
#     # Example URL: http://your-domain.com/api/get-report?code=3245
#     if code != '3245':
#         return HttpResponseForbidden("Invalid security code")
    
#     # Get all labor costs
#     labor_costs = LaborCosts.objects.all()
#     serializer = LaborCostsSerializer(labor_costs, many=True)
#     print(serializer.data)
#     output = io.BytesIO()
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Все трудозатраты"

#     # Headers
#     headers = ['report_id', 'employee_id','department_id', 'task_id', "task_name", "task_from_date", 'report_date', 'worked_hours', 'left_hours', 'comment']
#     ws.append(headers)
#     column_widths = {i: len(header) for i, header in enumerate(headers, start=1)}

#     # Fill data
#     for cost in serializer.data:
#         task = Task.objects.get(taskId=cost['taskId'])
#         row = [
#             cost['laborCostId'],
#             cost['employeeId'],
#             cost['departmentId'],
#             cost['taskId'],
#             task.taskName,
#             task.fromDate.date(),
#             cost['date'],
#             cost['workingHours'],
#             None if task.hourstodo == 0 else task.hourstodo,
#             cost['comment']
#         ]
#         ws.append(row)
#         for i, value in enumerate(row, start=1):
#             column_widths[i] = max(column_widths[i], len(str(value)))

#     # Set column widths
#     for i, width in column_widths.items():
#         ws.column_dimensions[get_column_letter(i)].width = width + 2

#     wb.save(output)
#     output.seek(0)
    
#     today_date = datetime.now().strftime('%Y-%m-%d')
#     filename = f'all_labor_costs_{today_date}.xlsx'

#     response = StreamingHttpResponse(
#         output,
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#     )
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response