FROM python:3.11-slim

WORKDIR /app

# Устанавливаем необходимые системные библиотеки для psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ca-certificates\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта
COPY . .

# Добавляем путь для поиска модулей
ENV PYTHONPATH=/app

# Копируем .env файл в контейнер
COPY .env .env

# Задаем переменные окружения для контейнера
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
