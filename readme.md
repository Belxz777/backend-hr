<p align="center">
  <a href="" target="blank"><img src="https://storage.yandexcloud.net/questsimages/forKV/2024-12-25_16-50-56%20(1).png" width="200" alt="" /></a>
</p>

Для запуска проекта необходимо:

1.Python 3.11+

2.Postgres SQL (14+)

3.Docker


Команды для ручного запуска приложения при внутренней базе данных:


1.pip install -r requirements.txt (при первом запуске для установки зависимостей)
(установите виртуальное окружение .venv или .conda)


2.Python manage.py makemigrations  essential (для создания миграции)


3.Python manage.py migrate essential (для применения миграции)


4.Python manage.py runserver (для запуска сервера)

При внешней миграции применять не нужно.

Также возможен запуск через докер:
//собрать image 
//docker build <imagename> <directory>
//запустить
//docker run <config> <imageid> 


Через docker-compose:
docker-compose run backend  python manage.py makemigrations
docker-compose run backend  python manage.py migrate
docker-compose up  --build


Через bat и sh file:

1.Просто запустите runwindows.bat || runlinux.sh файл для запуска проекта(для запуска необходимо иметь psql, python и docker,версии не так важны , возможны ошибки в отдельных случаях )

2. Порт на котором запускается возможно кастомизировать.

# Документация эндпоинтов:
### https://documenter.getpostman.com/view/29025992/2sAYX5LiFH

# Эксель отчет:
## Точный:
### https://storage.yandexcloud.net/filesup/tochnii_otchet_2025-02-05.xlsx
## Общий
### https://storage.yandexcloud.net/filesup/obshii_otchet_2025-02-05.xlsx


Используемые инструменты/Tools:
 

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) 




Для просмотра документации эндпоинтов общаться по роуту:/docs .


Для предоставления .env информации писать в telegram.

По всем вопросам обращаться:

@telegram:belxz999



Удалить мусор, использовать только если не запускается:
docker system prune
docker-compose restart core
