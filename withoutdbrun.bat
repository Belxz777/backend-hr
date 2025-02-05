@echo off
set SECRET_KEY=django-insecure-97o3!(wbra&h1b0oym%#(g@_@sspzfjf!_^c99nmr*(ocsak0a
set PG_HOST=localhost
set PGDATABASE=labor
set PGUSER=postgres
set PGPASSWORD=123
set ADMINPASS=a1234dfc
set DEBUG=True

@REM docker-compose -f docker-compose.yml up --build backend
@REM docker-compose -f docker-compose.yml up db
REM to test
docker-compose up --build


pause