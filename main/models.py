from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    jobId = models.AutoField(primary_key=True)  # Уникальный идентификатор должности
    jobName = models.CharField(max_length=30, null=False) 
    mainFunc = models.ForeignKey('Functions',on_delete=models.CASCADE,null=True)

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)  # Уникальный идентификатор услуги
    departmentName = models.CharField(max_length=100, null=False) 
    departmentDescription = models.CharField(max_length=200, null=True) 
    headId = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True)
    # tfs = models.ManyToManyField('TypicalFunction',null=True) 
    jobsList = models.ManyToManyField('Job',null=True)

class LaborCosts(models.Model):
    # Модель для трудозатрат, содержит информацию о затратах труда
    laborCostId = models.AutoField(primary_key=True)  # Уникальный идентификатор трудозатрат
    employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    tf = models.ForeignKey('Functions', on_delete=models.CASCADE,null=True)  # Идентификатор услуги
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(20),
            MinValueValidator(0.5)
        ], null=False)
    normal_hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(20),
            MinValueValidator(0.5)
        ], null=False)
    comment = models.CharField(max_length=300, null=True)  # Комментарий к трудозатратам
    date = models.DateTimeField( auto_now_add=True)
    

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



class Deputy(models.Model):
    # Модель для типовых функций, содержит информацию о типовых функциях
    tfId = models.AutoField(primary_key=True)  # Уникальный идентификатор типовой функции
    tfName = models.CharField(max_length=200, null=False)  # Название типовой функции
    tfDescription = models.CharField(max_length=150, null=True)  # Описание типовой функции
    isExt = models.BooleanField(default=False)
    deputy_functions = models.ManyToManyField('Functions', related_name='deputy_functions')

class Functions(models.Model):
    # Модель для основных функций, содержит информацию о основных функциях
    funcId = models.AutoField(primary_key=True)  # Уникальный идентификатор основной функции
    funcName = models.CharField(max_length=150, null=True)  # Описание основной функции
    time = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(20),
            MinValueValidator(0.5)
        ], null=False)
    consistent = models.ForeignKey('Deputy', on_delete=models.CASCADE, null=True, related_name='consistent_functions')    # Связь с моделью Job
    # No need for many-to-many here since Job model already has the relationship defined
# python manage.py makemigrations --empty main
# python manage.py migrate main zero
# python manage.py makemigrations
# python manage.py migrate
# Идентификатор отдела сотрудника


"""
должность и отдел

сотрудник имеет: вспомогательные функции обязательные

и 1 главную
"""