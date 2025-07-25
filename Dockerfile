FROM python:3.11
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "laborcount.wsgi:application"]