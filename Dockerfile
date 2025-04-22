# Use the official Python runtime image
FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# ENV EXTERNAL_DB = True
# ENV SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@
# ENV DATABASE_URL=postgresql://gen_user:UqNAZgZr%5C6.9Vk@195.133.27.160:5432/labor

RUN apt-get update && apt-get install -y \
       build-essential  \
       libpq-dev \
       && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]