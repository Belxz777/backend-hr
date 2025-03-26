from rest_framework import serializers
from .models import Employee, Job, Task, Department, LaborCosts, TypicalFunction

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid', 'expiredTasksCount', 'position', 'tasksCount', 'completedTasks']
          extra_kwargs = {'password': {'write_only': True},
                          'login': {'write_only': True}}   

class AdminEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid', 'expiredTasksCount', 'position', 'tasksCount', 'completedTasks']
        
class JobSerializer(serializers.ModelSerializer):
      class Meta:
          model = Job
          fields = ['jobId', 'jobName', 'typicalFunctions', 'indepart', 'rate']  

      def update(self, instance, validated_data):
          instance.jobName = validated_data.get('jobName', instance.jobName)
          instance.typicalFunctions.set(validated_data.get('typicalFunctions', instance.typicalFunctions.all()))
          instance.indepart = validated_data.get('indepart', instance.indepart)
          instance.save()
          return instance


class DepartmentSerializer(serializers.ModelSerializer):
      class Meta:
          model = Department  
          fields = ['departmentId', 'departmentName', 'departmentDescription', 'headId', 'typicalFunctions']

class PerformanceSerializer(serializers.Serializer):
      date = serializers.DateField()
      report_count = serializers.IntegerField()
      total_hours = serializers.DecimalField(max_digits=5, decimal_places=2)

class LaborCostsSerializer(serializers.ModelSerializer):
      class Meta:
          model = LaborCosts
          fields = ['laborCostId', 'employeeId', 'departmentId', 'taskId', 'date', 'worked_hours', 'comment']


class TypicalFunctionSerializer(serializers.ModelSerializer):
      class Meta:
          model = TypicalFunction
          fields = ['typicalFunctionId', 'typicalFunctionName', 'typicalFunctionDescription','departmentId','isMain']