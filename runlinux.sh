sudo docker build -t  backend-pulse .

sudo docker run -d -p 8000:8000 --env PYTHONUNBUFFERED=1 --env PYTHONDONTWRITEBYTECODE=1 --env DEBUG=FALSE --env SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@ --env DATABASE_URL=postgresql://test_pyco_user:zhsN9ck24KHRfx8JVVvGESCAwooM0Civ@dpg-cuhl54jtq21c73bbpai0-a.frankfurt-postgres.render.com/test_pyco --env   backend-pulse
