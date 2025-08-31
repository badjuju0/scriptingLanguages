FROM python:3.11-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev && rm -rf /var/lib/apt/lists/*

# Копируем код приложения
COPY . /app

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir flask feedparser

# Создаём папку для базы
RUN mkdir -p /data
ENV DB_PATH=/data/rss.db
EXPOSE 5000

# Копируем entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
