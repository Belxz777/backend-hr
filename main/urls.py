from django.urls import path

from main.utils.analytics.code import get_department_hours_report, get_employee_hours_report
from main.utils.analytics.common.common import get_all_departments_hours_report, get_combined_top_duties_and_functions, get_top_duties_and_functions
from main.utils.analytics.percentage.code import get_employee_tasks_distribution, get_tasks_distribution
from main.utils.analytics.workers.top import get_top_employees_by_department
from main.utils.compliencyandhistory.regdata import departsdata 
from main.utils.func.crud import DeputyView , FunctionsView
from main.utils.personal.code import get_user_functions
from main.utils.work.statistics import get_app_status_data
from .views import JobList, JobManaging,DepartmentManaging,DepartmentList
from main.utils import access_managing
from .utils.post import labor_fill
from .utils.report import getReport,getXlsxReport
from .utils.compliencyandhistory.compliency import EmployeeCompliancyView, EmployeePerformanceView
from .utils.compliencyandhistory.history import DepartmentPerformanceView
from .utils.emp_tasks import  getDepEmp
from .utils.access_managing import Reset_Password,UserQuickView
urlpatterns = [
    path('users/create',access_managing.RegisterView.as_view()),#для регистрации пользователей
    path("users/login",access_managing.LoginView.as_view()),#дяя входина
    path("users/auth",access_managing.UserAuth.as_view()),
    path('users/refresh',access_managing.refresh_token.as_view()),
    path('users/change_password',access_managing.Change_Password.as_view()),
    path('users/get_user',access_managing.GetUser.as_view()),
    path('users/deposition/',access_managing.Deposition.as_view()),
    path('users/compliancy/',EmployeeCompliancyView.as_view()),# типо как на github
    path('users/delete/<id>',labor_fill.delete_user),
    path('users/pass_recovery/',access_managing.PasswordRecovery.as_view()),

    path('users/',access_managing.UserList),

    path('users/<pk>',access_managing.UserDetail),
    
    path('users/quicksearch/',access_managing.UserQuickView),

    path('reset/password',access_managing.Reset_Password),


    # ! это рабочее
        


    path('entities/job/',JobManaging.as_view()),

    path('entities/jobs/',JobList.as_view()),

    

    

    
    path('entities/department/',DepartmentManaging.as_view()),

    path('entities/departments/overall/',departsdata),

    path('entities/department/create/',DepartmentList.as_view()),
    
    path('entities/department/employees/select/',getDepEmp),
    

    path('entities/functions/',FunctionsView.as_view()),


    path('entities/deputy/',DeputyView.as_view()),




    path('report/functions/',get_user_functions),

    path('fill/progress/', labor_fill.labor_fill),



    path('download/department/json/',getReport.get_labor_costs), # test для проверки записей о трудозатратах

    path('download/department/xlsx/',getXlsxReport.get_labor_costs_xlsx),

    path('download/department/xlsx/persice/',getXlsxReport.get_xlsx_precise),


    path('analytics/department/',get_department_hours_report),

    path('analytics/employee/',get_employee_hours_report),


    path('analytics/department/percentage/',get_tasks_distribution),

    path('analytics/employee/percentage/',get_employee_tasks_distribution),

    path('analytics/department/performance/top',get_top_employees_by_department),

    path('common/departments/',get_all_departments_hours_report),

    path('common/functions/separated',get_top_duties_and_functions),   


    path('common/functions/united',get_combined_top_duties_and_functions),   



    # path('analytics/employee/compliancy/',)

    path('history/user/',EmployeePerformanceView.as_view()) , # чекаем все таски сотрудника  за промежуток времен
    
    path('history/department/',DepartmentPerformanceView.as_view()),# чекаем все таски за промежуток времени





    path('app/statistics',get_app_status_data)


# & сделать создание функциональных обязаностей и должностей

# ! оформить логику заполнения отчета

# ? убрать не нужные эндпоинты



]