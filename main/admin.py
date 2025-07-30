from django.contrib import admin

# Register your models here.
from django.contrib import admin

from main.models import Job,Department,Reports,Employee

admin.site.register(Job)
admin.site.register(Department)
admin.site.register(Reports) 
admin.site.register(Employee)

