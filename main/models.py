from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    jobId = models.AutoField(primary_key=True)  # Уникальный идентификатор должности
    jobName = models.CharField(max_length=30, null=False) 
    tfs = models.ManyToManyField('TypicalFunction',null=True)
class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)  # Уникальный идентификатор услуги
    departmentName = models.CharField(max_length=100, null=False) 
    departmentDescription = models.CharField(max_length=200, null=True) 
    headId = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True)
    tfs = models.ManyToManyField('TypicalFunction',null=True) 
    jobsList = models.ManyToManyField('Job',null=True)
class LaborCosts(models.Model):
    # Модель для трудозатрат, содержит информацию о затратах труда
    laborCostId = models.AutoField(primary_key=True)  # Уникальный идентификатор трудозатрат
    employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    tf= models.ForeignKey('TypicalFunction', on_delete=models.CASCADE,null=True)  # Идентификатор услуги
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
    #добавить иерархию
    # #1 просто сотрудник  2 начальник сотрудника и тд чем выше position тем больше прав
    departmentid = models.ForeignKey(Department, on_delete=models.CASCADE) 



class TypicalFunction(models.Model):
    # Модель для типовых функций, содержит информацию о типовых функциях
    tfId = models.AutoField(primary_key=True)  # Уникальный идентификатор типовой функции
    tfName = models.CharField(max_length=200, null=False)  # Название типовой функции
    tfDescription = models.CharField(max_length=150, null=True)  # Описание типовой функции
    time = models.DecimalField(max_digits=5, decimal_places=2, validators=[
            MaxValueValidator(20),
            MinValueValidator(0.5)
        ], null=False)
    # No need for many-to-many here since Job model already has the relationship defined
    isMain = models.BooleanField(default=False) # по дефолту вспомогательная не главная


# python manage.py makemigrations --empty main
# python manage.py migrate main zero
# python manage.py makemigrations
# python manage.py migrate
# Идентификатор отдела сотрудника

#нужно продумать так что бы можно было интегрировать нейронку