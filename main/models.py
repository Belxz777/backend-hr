# models.py все модели приложения сердце логики  
 
from datetime import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Logs(models.Model):
    LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    module = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.level} - {self.message[:50]}"
    
    class Meta:
        ordering = ['-created_at']
        
  
class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    id = models.AutoField(primary_key=True,help_text="Уникальный инкрементируемый айди")  # Уникальный идентификатор должности
    name = models.CharField(max_length=75, null=False,help_text="Название должности") 
    pre_positioned = models.PositiveSmallIntegerField(
        default=1,
        help_text="Уровень в иерархии (1-5)"
    )

class Department(models.Model):
    id = models.AutoField(primary_key=True,help_text="Уникальный инкрементируемый айди отдела")  # Уникальный идентификатор услуги
    name = models.CharField(max_length=100, null=False,help_text="Название отдела") 
    # leader = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,help_text="Айди сотрудника начальника отдела")
    jobs_list = models.ManyToManyField('Job', blank=True, help_text="Должности сотрудников отдела")

class Employee(models.Model):
    # Модель для сотрудников, содержит информацию о работниках
    id = models.AutoField(primary_key=True,help_text="Уникальный инкрементируемый айди сотрудника")   
    name = models.CharField(max_length=30, null=False,help_text="Имя сотрудника",default=" ")  
    code = models.IntegerField(max_length=35,null=False,default=0,help_text="code")
    surname = models.CharField(max_length=30, null=True,help_text="Фамилия")  
    patronymic = models.CharField(max_length=30, null=False,default=" ")  
    login = models.CharField(max_length=30, null=False)  # Логин сотрудника
    password = models.CharField(max_length=128, null=False)  # Пароль сотрудника
    job = models.ForeignKey(Job, on_delete=models.CASCADE,help_text="Отдел в котором состоит") 
    department = models.ForeignKey(Department, on_delete=models.CASCADE,help_text="Отдел сотрдуника в котором он состоит") 
    position = models.IntegerField(default=1,help_text="Уровень доступа(позиция ) сотрудника 1-5") ;


class Reports(models.Model):
    id = models.AutoField(primary_key=True)  
    by_employee = models.ForeignKey('Employee', on_delete=models.CASCADE) # сотрудник заполняющий
    function = models.ForeignKey('Functions', on_delete=models.CASCADE)#функция по которой заполняется
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(10),
            MinValueValidator(0.5)
        ], null=False)# отработанное время
    comment = models.CharField(max_length=300, null=True)  
    date = models.DateTimeField(default=timezone.now) # дата отчета
    
class Functions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=False)
    description = models.TextField(max_length=300)
    is_main = models.BooleanField(default=True) # осноная или дополнительная если true то основная если false то дополнительная
    
    
    
    


"""
должность и отдел

сотрудник имеет: вспомогательные функции обязательные
# python manage.py makemigrations --empty main
# python manage.py migrate main zero
# python manage.py makemigrations
# python manage.py migrate  
# Идентификатор отдела сотрудника
# Идентификатор отдела сотрудника

и 1 главную
"""
