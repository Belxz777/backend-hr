#!/bin/bash

echo "Выберите метод запуска:"
echo "1. Docker Compose (redis + django)"
echo "2. Dockerfile (только django)"

read -p "Выберите (1 или 2): " choice

case $choice in
  1)
    echo "Запуск через Docker Compose..."
    sudo docker compose down -v  # если были предыдущие контейнеры
    sudo docker compose up --build -d
    ;;
  2)
    echo "Сборка и запуск через Dockerfile..."
    sudo docker build -t backend-pulse .
    sudo docker run -d -p 8000:8000 \
      --env PYTHONUNBUFFERED=1 \
      --env PYTHONDONTWRITEBYTECODE=1 \
      --env DEBUG=False \
      --env SECRET_KEY='django-insecure-%xr3kz0z7d3jpo!t%c6%&wkvra=6lm=5qx+#ua8zu#184l#he@' \
      --env REDIS_URL='redis://:belx001#22@host.docker.internal:6379/0' \
      --name django_app \
      backend-pulse
    ;;
  *)
    echo "Неправильный выбор. Введите 1 или 2."
    exit 1
    ;;
esac