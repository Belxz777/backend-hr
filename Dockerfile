# Use the official Python runtime image
FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y \
       build-essential  \
       libpq-dev \
       && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip


COPY requirements.txt ./requirements.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-warn-script-location -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]