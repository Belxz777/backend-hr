# signals.py сигналы используются для инвалидации кеша после изменения моделей
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def get_cache_key(model_instance):
    """Генерирует ключ кеша для экземпляра модели"""
    return f"{model_instance._meta.model_name}:{model_instance.pk}"

@receiver(pre_save)
def cache_before_save(sender, instance, **kwargs):
    """Сохраняет текущее состояние объекта перед изменением"""
    if not hasattr(instance, 'pk') or instance.pk is None:
        return  # Новый объект, нечего кешировать
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        cache_key = f"pre_save:{get_cache_key(old_instance)}"
        serializer = globals().get(f"{sender.__name__}Serializer")
        if serializer:
            cache.set(cache_key, serializer(old_instance).data, timeout=60*5)
            logger.debug(f"Pre-save cache set for {cache_key}")
    except sender.DoesNotExist:
        pass

@receiver(post_save)
def invalidate_after_save(sender, instance, created, **kwargs):
    """Инвалидирует кеш после сохранения объекта"""
    cache_key = get_cache_key(instance)
    
    # Удаляем основной кеш объекта
    cache.delete(cache_key)
    logger.info(f"Cache invalidated after save for {cache_key}")
    

@receiver(pre_delete)
def cache_before_delete(sender, instance, **kwargs):
    """Сохраняет данные объекта перед удалением (для возможного восстановления)"""
    cache_key = f"pre_delete:{get_cache_key(instance)}"
    serializer = globals().get(f"{sender.__name__}Serializer")
    if serializer:
        cache.set(cache_key, serializer(instance).data, timeout=60*60*24)  # Храним сутки
        logger.info(f"Pre-delete cache set for {cache_key}")

@receiver(post_delete)
def invalidate_after_delete(sender, instance, **kwargs):
    """Инвалидирует кеш после удаления объекта"""
    cache_key = get_cache_key(instance)
    
    # Удаляем основной кеш объекта
    cache.delete(cache_key)
    logger.info(f"Cache invalidated after delete for {cache_key}")
    
    # Для связанных кешей
    if sender.__name__ == 'Job':
        # Инвалидируем кеш списка должностей
        cache.delete('job_list_all')
        # Инвалидируем кеш сотрудников с этой должностью
        employees_cache_keys = [f"user_data_{emp.pk}" for emp in instance.employee_set.all()]
        cache.delete_many(employees_cache_keys)
        
    elif sender.__name__ == 'Department':
        # Инвалидируем кеш списка отделов
        cache.delete('departments_data')
        # Инвалидируем кеш сотрудников этого отдела
        employees_cache_keys = [f"user_data_{emp.pk}" for emp in instance.employee_set.all()]
        cache.delete_many(employees_cache_keys)