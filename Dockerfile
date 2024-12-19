FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POSTGRES_USER=postgres1 
ENV DEBUG = FALSE
ENV SECRET_KEY=django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@
ENV POSTGRES_PASSWORD=awpbMho0QStEeHfPUl96bY0ApIEnoBOm
ENV POSTGRES_DB=main_agry
ENV POSTGRES_HOST=dpg-cti3fnogph6c73d4kekg-a
ENV DATABASE_URL=postgresql://postgres1:awpbMho0QStEeHfPUl96bY0ApIEnoBOm@dpg-cti3fnogph6c73d4kekg-a/main_agry?ssl_mode=require

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