@echo off
REM Build the Docker image
docker build -t  backend-pulse .

REM Run the Docker container
docker run -d -p 8000:8000 --env PYTHONUNBUFFERED=1 --env PYTHONDONTWRITEBYTECODE=1 --env DEBUG=FALSE --env SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@ --env DATABASE_URL=postgresql://test_pyco_user:zhsN9ck24KHRfx8JVVvGESCAwooM0Civ@dpg-cuhl54jtq21c73bbpai0-a.frankfurt-postgres.render.com/test_pyco --env  EXTERNAL_DB = True --env   backend-pulse

@REM docker-compose mode
@REM @echo off 
@REM set SECRET_KEY=django-insecure-97o3!(wbra&h1b0oym%#(g@_@sspzfjf!_^c99nmr*(ocsak0a
@REM set PG_HOST=localhost
@REM set PGDATABASE=labor
@REM set PGUSER=postgres
@REM set PGPASSWORD=123
@REM set ADMINPASS=a1234dfc
@REM set DEBUG=FALSE

@REM @REM docker-compose -f docker-compose.yml up --build backend
@REM @REM docker-compose -f docker-compose.yml up db
@REM REM to test
@REM docker-compose up --build


@REM pause