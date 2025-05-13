# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем зависимости
RUN pip install --no-cache-dir flask feedparser

# Устанавливаем зависимости для Python и SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы в контейнер
COPY . .

# Указываем переменную среды для БД (можно изменить на другой путь или переменную окружения)
ENV DB_PATH=/app/rss.db

# Создаём нужные таблицы в БД перед запуском
RUN python -c "import sqlite3; conn = sqlite3.connect('$DB_PATH'); conn.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY, url TEXT UNIQUE);'); conn.execute('CREATE TABLE IF NOT EXISTS keywords (id INTEGER PRIMARY KEY, word TEXT UNIQUE);'); conn.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, title TEXT, summary TEXT, link TEXT UNIQUE, published TEXT);'); conn.commit(); conn.close()"

# Открываем порты для Flask
EXPOSE 5000

# Запускаем одновременно сборщик и веб-сервис
CMD ["sh", "-c", "python rss_collector.py & python api.py"]
