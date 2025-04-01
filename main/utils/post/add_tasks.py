# # views.py

# import openpyxl
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from datetime import datetime, timedelta
# from django.utils import timezone

# from main.utils.closeDate import calculate_close_date

# @csrf_exempt  # Отключаем CSRF для простоты (не рекомендуется в продакшене)
# def upload_tasks(request):
#     if request.method == 'POST':
#         excel_file = request.FILES.get('file')

#         if not excel_file:
#             return JsonResponse({'error': 'No file provided'}, status=400)

#         # Загружаем книгу Excel
#         workbook = openpyxl.load_workbook(excel_file)
#         sheet = workbook.active

#         tasks_created = []
#         for row in sheet.iter_rows(min_row=2, values_only=True):  # Пропускаем заголовок
#             name, description, employee_id, hours_to_complete = row
            
#             # Создаем запись в базе данных
#             task = Task.objects.create(
#                 taskName=name,
#                 taskDescription=description,
#                 forEmployeeId=employee_id,
#                 hours_todo=hours_to_complete,
#                 close_date = calculate_close_date(hours_to_complete,datetime.now())
#             )
#             tasks_created.append(task.id)

#         return JsonResponse({'message': 'Tasks created', 'task_ids': tasks_created}, status=201)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)
