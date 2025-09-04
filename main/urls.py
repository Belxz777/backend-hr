# from django.urls import path

# from main.utils.analytics.code import get_department_hours_report, get_employee_hours_report
# from main.utils.analytics.common.common import get_all_departments_hours_report, get_combined_top_duties_and_functions, get_top_duties_and_functions
# from main.utils.analytics.percentage.code import get_employee_tasks_distribution, get_tasks_distribution
# from main.utils.analytics.workers.top import get_top_employees_by_department
# from main.utils.compliencyandhistory.regdata import departsdata 
# from main.utils.func.crud import DeputyView , FunctionsView
# from main.utils.personal.code import get_user_functions
# from main.utils.work.statistics import get_app_status_data
# from main.utils.work.statistics import get_logs
# from .views import JobList, JobManaging,DepartmentManaging,DepartmentList
# from main.utils import access_managing
# from .utils.post import labor_fill
# from .utils.report import getReport,getXlsxReport
# from .utils.compliencyandhistory.compliency import EmployeeCompliancyView, EmployeePerformanceView
# from .utils.compliencyandhistory.history import DepartmentPerformanceView
# from .utils.emp_tasks import  getDepEmp

# from .utils.access_managing import Reset_Password,UserQuickView
# urlpatterns = [
#     path('users/create',access_managing.RegisterView.as_view()),#для регистрации пользователей
#     path("users/login",access_managing.LoginView.as_view()),#дяя входина
#     path("users/auth",access_managing.UserAuth.as_view()),
#     path('users/refresh',access_managing.refresh_token.as_view()),
#     path('users/change_password',access_managing.Change_Password.as_view()),
#     path('users/get_user',access_managing.GetUser.as_view()),
#     path('users/deposition/',access_managing.Deposition.as_view()),
#    # path('users/delete/<id>',labor_fill.delete_user),

#     path('users/',access_managing.user_list),

#     path('users/<pk>',access_managing.UserDetail),
    
#     path('users/quicksearch/',access_managing.UserQuickView),

#     path('reset/password',access_managing.Reset_Password),


#     # ! это рабочее точно
        


#     path('entities/job/',JobManaging.as_view()),

#     path('entities/jobs/',JobList.as_view()),

    

    

    
#     path('entities/department/',DepartmentManaging.as_view()),

#     path('entities/departments/overall/',departsdata),

#     path('entities/department/create/',DepartmentList.as_view()),
    
#     path('entities/department/employees/select/',getDepEmp),
    

#     path('entities/functions/',FunctionsView.as_view()),


#     path('entities/deputy/',DeputyView.as_view()),




#     path('report/functions/',get_user_functions),

#     path('fill/progress/', labor_fill.labor_fill),



#     path('analytics/department/',get_department_hours_report),

#     path('analytics/employee/',get_employee_hours_report),


#     path('analytics/department/percentage/',get_tasks_distribution),

#     path('analytics/employee/percentage/',get_employee_tasks_distribution),








 




#     path('history/user/',EmployeePerformanceView.as_view()) , # чекаем все таски сотрудника  за промежуток времен
    
#     path('history/department/',DepartmentPerformanceView.as_view()),# чекаем все таски за промежуток времени





#     path('app/statistics',get_app_status_data),
    
#     path('app/logs',get_logs),



# ]

from django.urls import path

from main.utils import access_managing
from main.utils.download.workdata import ReportsExcelExportView
from main.utils.reports_data.compliency import EmployeePerformanceView
from main.utils.reports_data.history import DepartmentPerformanceView
from main.utils.departments import DepartmentCreate, DepartmentManaging
from main.utils.functions import FunctionsManage
from main.utils.jobs import JobCreate, JobManaging
from main.utils.report.send import create_report
from main.utils.statistics import get_app_status_data

urlpatterns = [
    path('users/create',access_managing.RegisterView.as_view()),# создание сотрудника
    
    path("users/login",access_managing.LoginView.as_view()), # вход
    
    path("users/auth",access_managing.UserAuth.as_view()), # получение payload у токена
    # path('refresh',access_managing.refresh_token.as_view()), этот эндпоинт удален так как нет смысла потому что токен на фронтенде если
    # истекает то просто middleware выкидывает пользователя из профиля при next входе
    path('users/change_password',access_managing.ChangePassword.as_view()), # смена пароля с предоставлением старого
    
    path('users/get_user',access_managing.GetUser.as_view()), # получение данных о пользователе необходимо представить cookie токен 
    
    path('users/deposition',access_managing.Deposition.as_view()), # изменение позиции пользователя для выставления прав 

    path('users/detail/<pk>',access_managing.user_detail),# получение детальной информации о пользователе (не используется , не протестированно)
    
    path('users/quicksearch',access_managing.user_quick_view),# поиск по пользователям используется во всем компонентах с поиском 

    path('users/reset_password',access_managing.reset_password),# сброс пароля с использование подтверждения в виде пароля админа указывается в .env
    
    path('entities/job/',JobManaging.as_view()), # манипуляции с должностями (get,patch,delete) по id и также получение листа

    path('entities/job/create',JobCreate.as_view()), # создание должности 
    
    path('entities/department/',DepartmentManaging.as_view()), # также манипуляции с отделами (get,patch,delete ) по id и получение списка всех при регистарации
    
    path('entities/department/create',DepartmentCreate.as_view()),#  создание отдела
    
    # протестированно
    
    
    path('entities/functions/',FunctionsManage.as_view()),# манипуляции с функциями (crud)
    
    
    # path('report/functions/',get_user_functions), устарело

    path('fill/progress/', create_report), # отправка отчета по выполненной работе
    
    
    path('app/statistics',get_app_status_data),# получение статистики (cpu,ram,uptime)
    
    path('history/employee/',EmployeePerformanceView.as_view()) ,# получение статистки по сотруднику (отчеты)
    
    path('history/department/',DepartmentPerformanceView.as_view()),# получение статистики по отделу (тоже отчеты по периоду )
    
    path('download/workdata',ReportsExcelExportView.as_view())
    # подробно о функции вы можете узнать в комментариях внутри нее
]