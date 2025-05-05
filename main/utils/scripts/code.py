from main.models import Deputy, Functions


def sync_functions_to_deputies():
    """
    Синхронизирует функции с deputy_functions для всех Deputy,
    у которых есть связанные функции через consistent
    """
    # Получаем всех Deputy, у которых есть связанные функции
    deputies_with_functions = Deputy.objects.filter(
        consistent_functions__isnull=False
    ).distinct()
    
    for deputy in deputies_with_functions:
        # Получаем все функции, которые ссылаются на этого Deputy через consistent
        functions = Functions.objects.filter(consistent=deputy)
        
        # Добавляем эти функции в deputy_functions, если их там еще нет
        for func in functions:
            if not deputy.deputy_functions.filter(pk=func.pk).exists():
                deputy.deputy_functions.add(func)
    
    return f"Синхронизировано {deputies_with_functions.count()} deputies"