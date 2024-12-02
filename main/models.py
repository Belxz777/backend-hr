from django.db import models

# Create your models here.

class Job(models.Model):
    # Модель для должностей, содержит информацию о каждой должности
    jobId = models.AutoField(primary_key=True)  # Уникальный идентификатор должности
    jobName = models.CharField(max_length=30, null=False)  # Название должности
class Project(models.Model):
    # Модель для проектов, содержит информацию о каждом проекте
    projectId = models.IntegerField(primary_key=True)  # Уникальный идентификатор проекта
    projectName = models.CharField(max_length=30, null=False)  # Название проекта
    projectDescription = models.CharField(max_length=30, null=True)  # Описание проекта

class Task(models.Model):
    # Модель для задач, содержит информацию о каждой задаче
    taskId = models.IntegerField(primary_key=True)  # Уникальный идентификатор задачи
    taskName = models.CharField(max_length=30, null=False)  # Название задачи
    taskDescription = models.CharField(max_length=30, null=True) 
    dated = models.DateField(null=False)  # Описание задачи

class Department(models.Model):
    departmentId = models.AutoField(primary_key=True)  # Уникальный идентификатор услуги
    departmentName = models.CharField(max_length=30, null=False) 
    departmentDescription = models.CharField(max_length=200, null=True)  # Название услуги

class LaborCosts(models.Model):
    # Модель для трудозатрат, содержит информацию о затратах труда
    laborCostId = models.IntegerField(primary_key=True)  # Уникальный идентификатор трудозатрат
    employeeId = models.IntegerField(null=False)  # Идентификатор сотрудника
    departmentId = models.IntegerField(null=True)  # Идентификатор услуги
    taskId = models.IntegerField(null=False)  # Идентификатор задачи
    projectId = models.IntegerField(null=True)  # Идентификатор проекта
    date = models.DateField(null=False)  # Дата отчета о работе
    workingHours = models.DecimalField(max_digits=5, decimal_places=2, null=False)  # Затраченное время
    comment = models.CharField(max_length=30, null=True)  # Комментарий
    serviceDescription = models.CharField(max_length=30, null=True)  # Описание услуги


class Employee(models.Model):
    # Модель для сотрудников, содержит информацию о работниках
    employeeId = models.AutoField(primary_key=True)   
    firstName = models.CharField(max_length=30, null=False)  # Имя сотрудника
    lastName = models.CharField(max_length=30, null=False)  # Фамилия сотрудника
    patronymic = models.CharField(max_length=30, null=False)  # Отчество сотрудника
    login = models.CharField(max_length=30, null=False)  # Логин сотрудника
    password = models.CharField(max_length=30, null=False)  # Пароль сотрудника
    jobid = models.ForeignKey(Job, on_delete=models.CASCADE)  # Идентификатор должности сотрудника
    departmentid = models.ForeignKey(Department, on_delete=models.CASCADE)  # Идентификатор отдела сотрудника