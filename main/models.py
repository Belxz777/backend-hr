from datetime import timezone
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    jobId = models.AutoField(primary_key=True)  # Уникальный идентификатор должности
    jobName = models.CharField(max_length=75, null=False) 
    deputy = models.ForeignKey('Deputy',on_delete=models.CASCADE,null=True)

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)  # Уникальный идентификатор услуги
    departmentName = models.CharField(max_length=100, null=False) 
    departmentDescription = models.CharField(max_length=200, null=True) 
    headId = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True)
    jobsList = models.ManyToManyField('Job', blank=True)

class Employee(models.Model):
    # Модель для сотрудников, содержит информацию о работниках
    employeeId = models.AutoField(primary_key=True)   
    firstName = models.CharField(max_length=30, null=False)  # Имя сотрудника
    lastName = models.CharField(max_length=30, null=False)  # Фамилия сотрудника
    patronymic = models.CharField(max_length=30, null=False)  # Отчество сотрудника
    login = models.CharField(max_length=30, null=False)  # Логин сотрудника
    password = models.TextField(null=False)  # Пароль сотрудника
    jobid = models.ForeignKey(Job, on_delete=models.CASCADE) 
    position = models.IntegerField(default=1)
    departmentid = models.ForeignKey(Department, on_delete=models.CASCADE) 


class  LaborCosts(models.Model):
    # Модель для трудозатрат, содержит информацию о затратах труда
    laborCostId = models.AutoField(primary_key=True)  # Уникальный идентификатор трудозатрат
    employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    function = models.ForeignKey('Functions', on_delete=models.CASCADE,null=True)
    deputy = models.ForeignKey('Deputy', on_delete=models.CASCADE,null=True)
    compulsory = models.BooleanField(default=True)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(20),
            MinValueValidator(0.5)
        ], null=False)
    comment = models.CharField(max_length=300, null=True)  # Комментарий к трудозатратам
    date = models.DateTimeField(default=timezone.now) 
    


class Deputy(models.Model):
    # Модель для типовых функций, содержит информацию о типовых функциях
    deputyId = models.AutoField(primary_key=True)  # Уникальный идентификатор типовой функции
    deputyName = models.CharField(max_length=200, null=False)  # Название типовой функции
    deputyDescription = models.CharField(max_length=150, null=True)  # Описание типовой функции
    compulsory = models.BooleanField(default=True)
    deputy_functions = models.ManyToManyField('Functions', related_name='deputy_functions', blank=True)

class Functions(models.Model):


    # Модель для основных функций, содержит информацию о основных функциях
    funcId = models.AutoField(primary_key=True)  # Уникальный идентификатор основной функции
    funcName = models.CharField(max_length=150, null=True)  # Описание основной функции
    consistent = models.ForeignKey('Deputy', on_delete=models.CASCADE, null=True, related_name='consistent_functions')    # Связь с моделью Job
    # No need for many-to-many here since Job model already has the relationship defined
# python manage.py makemigrations --empty main
# python manage.py migrate main zero
# python manage.py makemigrations
# python manage.py migrate  
# Идентификатор отдела сотрудника
# Идентификатор отдела сотрудника


"""
должность и отдел

сотрудник имеет: вспомогательные функции обязательные

и 1 главную
"""
