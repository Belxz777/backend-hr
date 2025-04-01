from django.contrib import admin

# Register your models here.
from django.contrib import admin

from main.models import TypicalFunction,Job,Department,LaborCosts,Employee

admin.site.register(TypicalFunction)
admin.site.register(Job)
admin.site.register(Department)
admin.site.register(LaborCosts) 
admin.site.register(Employee)

