FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG = FALSE
ENV SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@
ENV DATABASE_URL=postgresql://test_pyco_user:zhsN9ck24KHRfx8JVVvGESCAwooM0Civ@dpg-cuhl54jtq21c73bbpai0-a.frankfurt-postgres.render.com/test_pyco
RUN apt-get update && apt-get install -y \
       build-essential  \
       libpq-dev \
       && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000:8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]