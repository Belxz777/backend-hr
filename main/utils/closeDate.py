from datetime import datetime, timedelta

def calculate_close_date(hours_needed, current_time):
    """
    Функция для вычисления даты и времени завершения задачи.
    
    :param hours_needed: Количество часов, необходимых для выполнения задачи.
    :param current_time: Текущее время в формате datetime.
    :return: Дата и время завершения задачи в формате datetime.
    """
    
    # Определяем начало и конец рабочего дня
    work_start = current_time.replace(hour=8, minute=0, second=0, microsecond=0)
    work_end = current_time.replace(hour=17, minute=0, second=0, microsecond=0)

    # Если текущее время до начала рабочего дня, устанавливаем его на начало рабочего дня
    if current_time < work_start:
        current_time = work_start
    
    # Если текущее время после конца рабочего дня, переходим на следующий рабочий день
    elif current_time > work_end:
        current_time += timedelta(days=1)
        current_time = current_time.replace(hour=8, minute=0, second=0, microsecond=0)

    # Подсчитываем оставшиеся часы
    while hours_needed > 0:
        # Проверяем, сколько времени осталось в текущем рабочем дне
        remaining_today = (work_end - current_time).seconds / 3600
        
        if remaining_today >= hours_needed:
            # Если оставшегося времени достаточно для выполнения задачи
            close_date = current_time + timedelta(hours=hours_needed)
            return close_date
        
        # Если оставшегося времени недостаточно, вычитаем его и переходим к следующему дню
        hours_needed -= remaining_today
        current_time = work_end + timedelta(days=1)  # Переход на следующий рабочий день
        current_time = current_time.replace(hour=8, minute=0, second=0, microsecond=0)

    return current_time

# Пример использования функции
current_time = datetime.now()  # Текущее время
hours_needed = 10  # Необходимое количество часов для выполнения задачи

close_date = calculate_close_date(hours_needed, current_time)
print("Дата и время завершения задачи:", close_date)
