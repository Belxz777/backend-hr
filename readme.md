# Оценка эффективности трудозатрат серверная часть
<p align="center">
  <a href="" target="blank"><img src="https://storage.yandexcloud.net/questsimages/forKV/2024-12-25_16-50-56%20(1).png" width="200" alt="" /></a>
</p>


# Описание запуска

**Перед запуском необходимо прописать адрес базы данных , а также сгенерировать секретный ключ для  корректной работы jwt аутентификации**  
## Пример .env конфигурации:
```

SECRET_KEY = "ваш секретный ключ"

DEBUG = False # для продакшен версии


IS_URL = False # если true то ссылка на бд должна быть в формате postgresql://user:password@host:port/dbname


DATABASE_NAME = "имя базы данных"

DATABASE_HOST = 81.200.158.11 # хост

DATABASE_PASSWORD = "пароль для подключения к бд"

DATABASE_USER = "пользователь"

DATABASE_PORT = 5432 # порт на котором работает бд
    
```   
! Для собственной настройки редактируйте laborcount/settings.py файл


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

## Необходимо  установить  зависимости(pip) и создать виртуальное окружение (.venv, .conda):
```
> pip install --upgrade pip
> pip install -r requirements.txt # что бы устнавовить все зависимости
> source .venv/bin/activate # что бы активировать виртуальное окружение

```
в vs code возможно автоматическая установка .venv , необходимо скачать *Python Extension*


## Применение миграции , создание сущностей в базе данных:

```
> python manage.py makemigrations 

> python manage.py migrate 
```
### Для более точного проведения миграций обратитесь к официальной документации django


## Запуск приложения 

```
> python manage.py runserver 

```

### Возможен запуск с дополнительными параметрами , для более подробной информации обратитесь к документации django


# Также возможен  ручной запуск через докер:
```
docker build <imagename>  # создание образа

docker run <config> <imageid>  # запуск контейнера
```


# Через docker-compose(2 и более инстансов):
```
docker-compose run backend  python manage.py makemigrations

docker-compose run backend  python manage.py migrate

docker-compose up  --build
```




# Документация эндпоинтов:
### https://documenter.getpostman.com/view/29025992/2sAYX5LiFH



# Используемые инструменты:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) 
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) 

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) 
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) 
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) 




## По всем вопросам обращаться:

### @telegram:belxz999




