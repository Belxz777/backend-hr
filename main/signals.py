# myapp/signals.py
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from main.models import Deputy, Employee


@receiver(post_save, sender=Employee)
@receiver(post_delete, sender=Employee)
def clear_employee_cache(sender, instance, **kwargs):
    """
    Очищает кэш пользователя при изменении или удалении сотрудника
    """
    try:
        # Для Redis с поддержкой delete_pattern (использует SCAN)
        cache.delete_pattern(f"*user_*_data")  # Удаляем все ключи пользователей
        
        # Альтернативный вариант - точечное удаление
        cache.delete(f"user_{instance.employeeId}_data")
        
        # Если используем Deputy, очищаем связанные кэши
        if hasattr(instance, 'jobid') and instance.jobid.deputy:
            cache.delete_pattern("*deputy_*")
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Cache invalidation error: {str(e)}")

@receiver(post_save, sender=Deputy)
@receiver(post_delete, sender=Deputy)
def clear_deputy_cache(sender, instance, **kwargs):
    """
    Очищает кэш при изменении
    """
    try:
        cache.delete_pattern("*deputy_*")
        cache.delete_pattern("*user_*_data")  # Так как deputy влияет на ответ API
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Deputy cache invalidation error: {str(e)}")