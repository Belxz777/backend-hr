from django.urls import path
from .views import JobList, JobManaging,DepartmentManaging,DepartmentEmployees,DepartmentList,TaskManaging
from main.utils import token_managing

from .utils.post import labor_fill
from .utils.report import getReport,getXlsxReport
from .utils.emp_tasks import EmployeeTasksbystatus,AllEmployeeTasks
urlpatterns = [
    path('users/create',token_managing.RegisterView.as_view()),#для регистрации пользователей
    path("users/login",token_managing.LoginView.as_view()),#дяя входина
    path("users/auth",token_managing.UserAuth.as_view()),
    path('users/refresh',token_managing.refresh_token.as_view()),
    path('users/change_password',token_managing.Change_Password.as_view()),
    path('users/get_user',token_managing.GetUser.as_view()),


    


    path('entities/job/<id>',JobManaging.as_view()),

    path('entities/jobs/',JobList.as_view()),
    

    

    
    path('entities/department/<id>',DepartmentManaging.as_view()),

    path('entities/department/<id>/employees/',DepartmentEmployees.as_view()),

    path('entities/departments/',DepartmentList.as_view()),




    path('entities/task/<id>',TaskManaging.as_view()),

    path('entities/user/<id>/tasks/<status>/',  EmployeeTasksbystatus.as_view(), name='employee-tasks-bystatus'),
    
    path('entities/user/tasks/', AllEmployeeTasks.as_view()),



    path('fill/progress/', labor_fill.labor_fill),



path('report/department/json/<id>',getReport.get_labor_costs),

path('report/department/xlsx/<id>',getXlsxReport.get_labor_costs_xlsx),

    





# * релизовать логику записи трудозатрат  10 часов done

# & реализовать логику расчета трудозатрат 10 часов done
 
# ? реализовать выгрузку отчетности в формате excel 4 часов done

#^ Покрыть код тестами и проверить (интегрировать ) необходимые требования к безопасности 30 часов in progress

#! Добавить понятную документацию для разработчиков контейнизировать приложение 5 часов in progress


#* Всего времени : 130 часов

#* Примерные трудозатраты:61 час + риски 20 часов + тест в реальном времени(10) = 91 час 



#& осталось 35 часов работы до доведения до ума



]