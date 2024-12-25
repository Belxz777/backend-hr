<p align="center">
  <a href="" target="blank"><img src="https://storage.yandexcloud.net/questsimages/forKV/2024-12-25_16-50-56%20(1).png" width="200" alt="" /></a>
</p>

Для запуска проекта необходимо:

1.Python 3.11+

2.Postgres SQL (14+)

3.Docker


Команды для ручного запуска приложения при внутренней базе данных:


1.pip install -r requirements.txt (при первом запуске для установки зависимостей)


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



Используемые инструменты/Tools:
 

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) 




Для просмотра документации эндпоинтов общаться по роуту:/docs .


Для предоставления .env информации писать в telegram.

По всем вопросам обращаться:

@telegram:belxz999









UTIL DATA:

docker-compose for local:
version: '3.12'

services:
  db:
    image: postgres:15
    container_name: db
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres_user_owner
      - POSTGRES_PASSWORD=mWPVS5GepH1l
      - POSTGRES_DB=postgres_user
      - POSTGRES_HOST=ep-tight-sun-a81gunnv.eastus2.azure.neon.tech
    ports:
      - 5432:5432
  backend:
    build: .
    command: python manage.py runserver 127.0.0.1:8000
    network_mode: host
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1
      - POSTGRES_DB=system_memory
      - POSTGRES_HOST=localhost
    depends_on:
      - db
    env_file:
      - .env
    volumes:
      - ./:/usr/src/app
    ports:
      - 8000:8000


volumes:
  postgres-data:




docker-compose non executable in case if you are running single app in my case it is cause i use externaal db rath
er than localy so use this instructions.(Belxz777 6.11.24)


to view summary about an image :  docker scout quickview
docker prune to deelete all images


neon db url:
postgresql://neondb_owner:GAP0vqcr2Jfh@ep-nameless-field-a5mfa03i-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require
doesnt work withhout vpn but its okay to reach db;
