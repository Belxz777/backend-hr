FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POSTGRES_USER=postgres_user_owner
ENV DEBUG = FALSE
ENV SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@
ENV POSTGRES_PASSWORD=mWPVS5GepH1l
ENV POSTGRES_DB=postgres_user
ENV POSTGRES_HOST=ep-tight-sun-a81gunnv.eastus2.azure.neon.tech
ENV DATABASE_URL=postgresql://postgres_user_owner:mWPVS5GepH1l@ep-tight-sun-a81gunnv.eastus2.azure.neon.tech/postgres_user?sslmode=require

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