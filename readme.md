# Backend Pulse
<p align="center">
  <a href="" target="blank"><img src="https://storage.yandexcloud.net/questsimages/forKV/2024-12-25_16-50-56%20(1).png" width="200" alt="" /></a>
</p>


# Описание запуска

## Существует 2 варианта запуска приложения:
> 1. С внутренней базой данных
> 2. С внешней базой данных

## Вариант 1
### Запуск приложения
1. Запуск файла withoutdbrun.bat
2. Или в ручную 

## Вариант 2
### Запуск приложения
1. Запуск файла withdbrun.bat
2. Или в ручную


# Ручной запуск

## Необходимо  установить  зависимости и создать виртуальное окружение (.venv, .conda):

> pip install -r requirements.txt

в vs code возможно автоматическая установка .venv , необходимо скачать *Python Extension*


## Применение миграции , создание сущностей в базе данных:
### Этот шаг проделывается при условии что база данных внутренняя.

```
> python manage.py makemigrations 

> python manage.py migrate 
```

## Запуск приложения 

```
> python manage.py runserver 

```




# Также возможен  ручной запуск через докер:
```
docker build <imagename> 

docker run <config> <imageid> 
```


# Через docker-compose:
```
docker-compose run backend  python manage.py makemigrations

docker-compose run backend  python manage.py migrate

docker-compose up  --build
```




# Документация эндпоинтов:
### https://documenter.getpostman.com/view/29025992/2sAYX5LiFH

# Эксель отчет:
## Точный:
### https://storage.yandexcloud.net/filesup/tochnii_otchet_2025-02-05.xlsx
## Общий
### https://storage.yandexcloud.net/filesup/obshii_otchet_2025-02-05.xlsx


# Используемые инструменты:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) 

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) 



## Для предоставления .env информации писать в telegram.

## По всем вопросам обращаться:

### @telegram:belxz999




