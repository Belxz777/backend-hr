from rest_framework import serializers
from .models import Job, Department, Employee, Reports, Functions

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'pre_positioned']
        extra_kwargs = {
            'pre_positioned': {'min_value': 1, 'max_value': 5}
        }

class DepartmentSerializer(serializers.ModelSerializer):
    jobs_list = JobSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name',  'jobs_list']
        
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.leader:
    #         representation['leader'] = EmployeeSerializer(instance.leader).data
    #     return representation

class EmployeeSerializer(serializers.ModelSerializer):
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), 
        source='job',
        write_only=True
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )
    
    # Для чтения используем вложенные сериализаторы
    job = JobSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'surname', 'patronymic', 
            'login', 'password', 'job', 'department',
            'job_id', 'department_id', 'position'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'position': {'min_value': 1, 'max_value': 5}
        }

class AdminEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'position': {'min_value': 1, 'max_value': 5}
        }

class ReportsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reports
        fields = [
            'id', 'by_employee', 'function', 
            'hours_worked', 'comment', 'date'
        ]
        extra_kwargs = {
            'hours_worked': {
                'min_value': 0.5,
                'max_value': 10
            },
            'comment': {'required': False, 'allow_blank': True}
        }

class FunctionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Functions
        fields = ['id', 'name', 'description', 'is_main']