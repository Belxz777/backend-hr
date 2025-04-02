from rest_framework import serializers
from .models import Employee, Job,  Department, LaborCosts, TypicalFunction

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid', 'position']
          extra_kwargs = {'password': {'write_only': True},
                          'login': {'write_only': True}}   

class AdminEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid',  'position', ]
        
class JobSerializer(serializers.ModelSerializer):
    typicalfunctions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=TypicalFunction.objects.all(),
        required=False
    )

    class Meta:
        model = Job
        fields = ['jobId', 'jobName', 'tfs']

    def create(self, validated_data):
        typicalfunctions_data = validated_data.pop('tfs', [])
        job = Job.objects.create(**validated_data)
        job.tfs.set(typicalfunctions_data)
        return job
class DepartmentSerializer(serializers.ModelSerializer):
      class Meta:
          model = Department  
          fields = ['departmentId', 'departmentName', 'departmentDescription', 'headId', 'tfs','jobsList']


class PerformanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    report_count = serializers.IntegerField()
    total_hours = serializers.DecimalField(max_digits=5, decimal_places=2)

class LaborCostsSerializer(serializers.ModelSerializer):
      class Meta:
          model = LaborCosts
          fields = ['laborCostId', 'employeeId', 'departmentId', 'tf', 'date', 'worked_hours','normal_hours', 'comment']

from rest_framework import serializers

class TypicalFunctionSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = TypicalFunction
        fields = [
            'tfId', 
            'tfName', 
            'tfDescription',
            'time',
            'isMain'
        ]