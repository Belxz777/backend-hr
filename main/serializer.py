
from rest_framework import serializers
from .models import Employee, Job, Task, Department, LaborCosts

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid']
        extra_kwargs = {'password': {'write_only': True},
                        'login': {'write_only': True}}
        
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['jobId','jobName']  

    def update(self, instance, validated_data):
        instance.jobName = validated_data.get('jobName', instance.jobName)
        instance.save()
        return instance


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['projectId', 'projectName', 'projectDescription']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['taskId', 'taskName','forEmployeeId','status','hourstodo' ,'been','taskDescription',  'fromDate']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['departmentId', 'departmentName','departmentDescription']

class LaborCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaborCosts
        fields = ['laborCostId', 'employeeId', 'departmentId', 'taskId', 'date', 'workingHours', 'comment', 'serviceDescription']

