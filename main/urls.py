from django.urls import path
from .views import JobList, JobManaging,DepartmentManaging,DepartmentList,ProjectManaging,TaskManaging,ProjectByName
from main.utils import token_managing
from utils.subobj import ProjectTasks
urlpatterns = [
    path('users/create',token_managing.RegisterView.as_view()),#для регистрации пользователей
    path("users/login",token_managing.LoginView.as_view()),#дяя входина
    path("users/auth",token_managing.UserAuth.as_view()),
    path('users/refresh',token_managing.refresh_token.as_view()),
    path("users/logout",token_managing.LogoutView.as_view()),


    # path('entities/department',views.create_employee),
    path('entities/job/<id>',JobManaging.as_view()),

    path('entities/jobs/',JobList.as_view()),
    

    

    
    path('entities/department/<id>',DepartmentManaging.as_view()),

    path('entities/departments/',DepartmentList.as_view()),




    path('entities/project/<id>',ProjectManaging.as_view()),

    path('entities/projects/<str:name>',ProjectByName.as_view()),



    path('entities/task/<id>',TaskManaging.as_view()),

    path('entities/user/byName/<str:name>',token_managing.UserByName.as_view()),

    path('entities/user/<id>/tasks/?<str:status>/', ProjectTasks.as_view(), name='project-tasks-status'),




# начать делать заполнение отчета 
#сделать статус оптионом типо можно не писать
# ! добавить crud для проектов и задач  2 часа

# * релизовать логику записи трудозатрат  10 часов

# & реализовать логику расчета трудозатрат 10 часов
 
# ? реализовать выгрузку отчетности в формате excel 4 часов

#^ Покрыть код тестами и проверить (интегрировать ) необходимые требования к безопасности 30 часов

#! Добавить понятную документацию для разработчиков контейнизировать приложение 5 часов


#* Всего времени : 130 часов

#* Примерные трудозатраты:61 час + риски 20 часов + тест в реальном времени(10) = 91 час 






]