@REM docker-compose run backend  python manage.py makemigrations
@REM docker-compose run backend  python manage.py migrate
@REM docker-compose up  --build
@REM config for composed version while using intern db

docker build -t pulse-backend  .
docker run -it -p 8000:8000  pulse-backend