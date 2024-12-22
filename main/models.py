from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    jobId = models.AutoField(primary_key=True)  # Уникальный идентификатор должности
    jobName = models.CharField(max_length=30, null=False)  # Название должности
#проекты не нужны надо от них избавляться
class Task(models.Model):
    # Модель для задач, содержит информацию о каждой задаче
    taskId = models.AutoField(primary_key=True)  # Уникальный идентификатор задачи
    taskName = models.CharField(max_length=50, null=False)  # Название задачи
    taskDescription = models.CharField(max_length=150, null=True)
    forEmployeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) 
    status = models.CharField(max_length=20, choices=[
        ('in_progress', 'В процессе'),
        ('completed', 'Готово'),
        ('todo', 'Сделать')
    ], default='not_started')  # Статус задачи
    hourstodo = models.IntegerField(   validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ],default=1,null=False)
    been = models.BooleanField(default=False)
    fromDate = models.DateTimeField( auto_now_add=True)
    closeDate = models.DateTimeField(null=False)
    expired = models.BooleanField(default=False)  # Описание задачи 

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)  # Уникальный идентификатор услуги
    departmentName = models.CharField(max_length=30, null=False) 
    departmentDescription = models.CharField(max_length=200, null=True) 
    headId = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True)# Название услуги

class LaborCosts(models.Model):
    # Модель для трудозатрат, содержит информацию о затратах труда
    laborCostId = models.AutoField(primary_key=True)  # Уникальный идентификатор трудозатрат
    employeeId = models.ForeignKey('Employee', on_delete=models.CASCADE) # Идентификатор сотрудника
    departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    taskId = models.ForeignKey("Task", on_delete=models.CASCADE, null=False)  # Идентификатор задачи
    date = models.DateField(auto_now_add=True)  # Дата отчета о работе
    workingHours = models.IntegerField( validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ],null=False)  # Затраченное время
    comment = models.CharField(max_length=150, null=True)  # Комментарий


class Employee(models.Model):
    # Модель для сотрудников, содержит информацию о работниках
    employeeId = models.AutoField(primary_key=True)   
    firstName = models.CharField(max_length=30, null=False)  # Имя сотрудника
    lastName = models.CharField(max_length=30, null=False)  # Фамилия сотрудника
    patronymic = models.CharField(max_length=30, null=False)  # Отчество сотрудника
    login = models.CharField(max_length=30, null=False)  # Логин сотрудника
    password = models.CharField(max_length=30, null=False)  # Пароль сотрудника
    jobid = models.ForeignKey(Job, on_delete=models.CASCADE) 
    #добавить иерархию
    position = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])#1 просто сотрудник  2 начальник сотрудника и тд чем выше position тем больше прав
    departmentid = models.ForeignKey(Department, on_delete=models.CASCADE)  # Идентификатор отдела сотрудника

#нужно продумать так что бы можно было интегрировать нейронку
    