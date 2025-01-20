@REM docker-compose run backend  python manage.py makemigrations
@REM docker-compose run backend  python manage.py migrate
@REM docker-compose up  --build
@REM config for composed version while using intern db

@REMdocker build -t pulse-backend  .
@REMdocker run -it -p 8000:8000 @REMulse-backend
docker-compose run backend  python manage.py makemigrations
docker-compose run backend  python manage.py migrate
docker-compose up  --build

