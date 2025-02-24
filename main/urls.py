from django.urls import path

from main.utils.compliencyandhistory.regdata import departsdata
from main.utils.post.add_tasks import upload_tasks
from .views import JobList, JobManaging,DepartmentManaging,DepartmentEmployees,DepartmentList,TaskManaging
from main.utils import access_managing
from .utils.post import labor_fill
from .utils.report import getReport,getXlsxReport
from .utils.compliencyandhistory.compliency import EmployeePerformanceView
from .utils.compliencyandhistory.history import DepartmentPerformanceView
from .utils.emp_tasks import EmployeeTasksbystatus,AllEmployeeTasks, ToReportTasks, getDepEmp
urlpatterns = [
    path('users/create',access_managing.RegisterView.as_view()),#для регистрации пользователей
    path("users/login",access_managing.LoginView.as_view()),#дяя входина
    path("users/auth",access_managing.UserAuth.as_view()),
    path('users/refresh',access_managing.refresh_token.as_view()),
    path('users/change_password',access_managing.Change_Password.as_view()),
    path('users/get_user',access_managing.GetUser.as_view()),
    path('users/deposition/',access_managing.Deposition.as_view()),
    path('users/compliancy/',EmployeePerformanceView.as_view()),# типо как на github
 # это работает , есть небольная проблема с caching

    


    path('entities/job/<id>',JobManaging.as_view()),

    path('entities/jobs/',JobList.as_view()),

    

    
    path('entities/department/',DepartmentManaging.as_view()),

    path('entities/departments/overall/',departsdata),

    path('entities/department/create/',DepartmentList.as_view()),
    
    path('entities/department/employees/select/',getDepEmp),
    





    path('entities/task/',TaskManaging.as_view()),

    path('entities/user/tasks/bystatus/',  EmployeeTasksbystatus.as_view(), name='employee-tasks-bystatus'),
    
    path('entities/user/tasks/', AllEmployeeTasks.as_view()),

    path('entities/user/tasks/reported/', ToReportTasks.as_view()),




    path('fill/progress/', labor_fill.labor_fill),



    path('download/department/json/',getReport.get_labor_costs), # test для проверки записей о трудозатратах

    path('download/department/xlsx/',getXlsxReport.get_labor_costs_xlsx),

    path('download/department/xlsx/persice/',getXlsxReport.get_xlsx_precise),

    path('history/user/tasks/',EmployeePerformanceView.as_view()) , # чекаем все таски сотрудника  за промежуток времен
    
    path('history/department/tasks',DepartmentPerformanceView.as_view()),# чекаем все таски за промежуток времени


    # path('neuro/analytics/department/') # аналитика с нейросетки



    # path('entities/department/xlsx/add',upload_tasks)



#! todo: протестить роут с добавлением задач 
#! также решить вопрос с позициями сотрудников 
#! попробовать внедрить кеширование особенно на выдачу данных сотрудника
#! запустить в изолированном окружении

# * релизовать логику записи трудозатрат  10 часов done

# & реализовать логику расчета трудозатрат 10 часов done
 
# ? реализовать выгрузку отчетности в формате excel 4 часов done

#^ Покрыть код тестами и проверить (интегрировать ) необходимые требования к безопасности 30 часов in progress

#! Добавить понятную документацию для разработчиков контейнизировать приложение 5 часов in progress


#* Всего времени : 130 часов

#* Примерные трудозатраты:61 час + риски 20 часов + тест в реальном времени(10) = 91 час 



#& осталось 35 часов работы до доведения до ума

#* к Февралю должно быть готово



]