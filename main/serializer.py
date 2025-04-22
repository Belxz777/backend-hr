from rest_framework import serializers
from .models import Employee, Job, Department, LaborCosts, Deputy, Functions

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid', 'position']
          extra_kwargs = {'password': {'write_only': True},
                          'login': {'write_only': True}}   

class AdminEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
          model = Employee
          fields = ['employeeId', 'firstName', 'lastName', 'patronymic', 'login', 'password', 'jobid', 'departmentid', 'position']
        
class JobSerializer(serializers.ModelSerializer):
    mainFunc = serializers.PrimaryKeyRelatedField(queryset=Functions.objects.all(), required=False)

    class Meta:
        model = Job
        fields = ['jobId', 'jobName', 'mainFunc']

class DepartmentSerializer(serializers.ModelSerializer):
      class Meta:
          model = Department  
          fields = ['departmentId', 'departmentName', 'departmentDescription', 'headId', 'jobsList']

class PerformanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    report_count = serializers.IntegerField()
    total_hours = serializers.DecimalField(max_digits=5, decimal_places=2)

class LaborCostsSerializer(serializers.ModelSerializer):
      class Meta:
          model = LaborCosts
          fields = ['laborCostId', 'employeeId', 'departmentId', 'tf', 'date', 'worked_hours', 'normal_hours', 'comment']

class DeputySerializer(serializers.ModelSerializer):
    functions = serializers.PrimaryKeyRelatedField(many=True, queryset=Functions.objects.all(), required=False)

    class Meta:
        model = Deputy
        fields = [
            'tfId', 
            'tfName', 
            'tfDescription',
            'isExt',
            'functions'
        ]

class FunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Functions
        fields = [
            'funcId',
            'funcName',
            'time',
            'consistent'
        ]