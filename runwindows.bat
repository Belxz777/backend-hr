@echo off
REM Docker Compose for Django app version: '3.12'
REM Services configuration

docker-compose up --build

REM Dockerfile for backend service
echo version: '3.12' > docker-compose.yml
echo services: >> docker-compose.yml
echo   backend: >> docker-compose.yml
echo     build: . >> docker-compose.yml
echo     command: python manage.py runserver 0.0.0.0:8000 >> docker-compose.yml
echo     network_mode: host >> docker-compose.yml
echo     depends_on: >> docker-compose.yml
echo       - db >> docker-compose.yml   
echo     volumes: >> docker-compose.yml
echo       - ./:/usr/src/app >> docker-compose.yml
echo     ports: >> docker-compose.yml
echo       - 8000:8000 >> docker-compose.yml
echo   db: >> docker-compose.yml
echo     image: postgres:15 >> docker-compose.yml
echo     container_name: db >> docker-compose.yml
echo     volumes: >> docker-compose.yml
echo       - postgres-data:/var/lib/postgresql/data >> docker-compose.yml
echo     environment: >> docker-compose.yml
echo       - "POSTGRES_HOST_AUTH_METHOD=trust" >> docker-compose.yml
echo     ports: >> docker-compose.yml
echo       - 5432:5432 >> docker-compose.yml
echo volumes: >> docker-compose.yml
echo   postgres-data: >> docker-compose.yml
echo     driver: local >> docker-compose.yml

pause

