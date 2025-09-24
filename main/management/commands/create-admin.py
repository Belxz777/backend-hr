# your_app/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import Job, Department, Employee  

class Command(BaseCommand):
    help = 'Создает администратора с отделом "Управление организации труда и заработной платы № 5"'

    def handle(self, *args, **options):
        # Создаем или получаем должность
        job, created = Job.objects.get_or_create(
            name='Главный Администратор',
            defaults={
                'pre_positioned': 5  # Максимальный уровень доступа
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Должность "Главный Администратор" создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Должность "Главный Администратор" уже существует'))

        # Создаем или получаем отдел
        department, created = Department.objects.get_or_create(
            name='Управление организации труда и заработной платы № 5',
            defaults={}
        )
        
        # Добавляем должность в отдел
        department.jobs_list.add(job)
        
        if created:
            self.stdout.write(self.style.SUCCESS('Отдел "Управление организации труда и заработной платы № 5" создан'))
        else:
            self.stdout.write(self.style.SUCCESS('Отдел "Управление организации труда и заработной платы № 5" уже существует'))

        # Создаем администратора
        admin, created = Employee.objects.get_or_create(
            login='admin',
            defaults={
                'name': 'Администратор',
                'surname': 'Главный',
                'patronymic': 'Системы',
                'code': 1,
                'password': make_password('admin123'),  # Пароль по умолчанию
                'job': job,
                'department': department,
                'position': 5  # Максимальный уровень доступа
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Администратор создан!\n'
                    f'Логин: admin\n'
                    f'Пароль: admin123\n'
                    f'Измените пароль после первого входа!'
                )
            )
        else:
            self.stdout.write(self.style.WARNING('Администратор уже существует'))