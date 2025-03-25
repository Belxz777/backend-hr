from datetime import datetime, timedelta
from django.utils.timezone import make_aware

def calculate_close_date(hours_needed, current_time):
    current_time = make_aware(current_time)  # Делаем время осведомленным о временной зоне
    
    work_start = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
    work_end = current_time.replace(hour=17, minute=0, second=0, microsecond=0)
    
    if current_time < work_start:
        current_time = work_start
    elif current_time > work_end:
        current_time = (current_time + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    
    while hours_needed > 0:
        remaining_today = (work_end - current_time).seconds / 3600
        
        if remaining_today >= hours_needed:
            return current_time + timedelta(hours=hours_needed)
        
        hours_needed -= remaining_today
        current_time = (work_end + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    
    return current_time
# Пример использования функции
# current_time = datetime.now()  # Текущее время
# hours_needed = 10  # Необходимое количество часов для выполнения задачи

# close_date = calculate_close_date(hours_needed, current_time)
# print("Дата и время завершения задачи:", close_date)
def isExpired( first_time,second_time):
    """
    Функция для проверки, является ли первое время не позже второго.
    
    :param first_time: Первое время в формате datetime.
    :param second_time: Второе время в формате datetime.
    :return: True, если первое время не позже второго, иначе False.
    """
    # Убираем информацию о часовом поясе
    first_time = first_time.replace(tzinfo=None)
    second_time = second_time.replace(tzinfo=None)

    return first_time >= second_time


 # Установим второе время на 23:59:59

result = isExpired(datetime.now(), datetime.now() - timedelta(days=1))
# print(result) True