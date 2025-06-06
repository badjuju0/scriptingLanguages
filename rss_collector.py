import feedparser
import sqlite3
from datetime import datetime
import time
import threading

DB_NAME = "rss.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS feeds (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY,
                word TEXT UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT,
                summary TEXT,
                link TEXT UNIQUE,
                published TEXT
            )
        ''')
        conn.commit()

def get_feeds_and_keywords():
    with sqlite3.connect(DB_NAME) as conn:
        feeds = [row[0] for row in conn.execute("SELECT url FROM feeds")]
        keywords = [row[0].lower() for row in conn.execute("SELECT word FROM keywords")]
        return feeds, keywords

def save_news(item):
    with sqlite3.connect(DB_NAME) as conn:
        try:
            conn.execute('''
                INSERT INTO news (title, summary, link, published)
                VALUES (?, ?, ?, ?)
            ''', (item['title'], item['summary'], item['link'], item['published']))
            conn.commit()
            print(f"[{datetime.now()}] Новость добавлена: {item['title']}")
        except sqlite3.IntegrityError:
            pass  # уже есть

def check_feeds():
    feeds, keywords = get_feeds_and_keywords()
    found = False
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            content = (entry.get('title', '') + ' ' + entry.get('summary', '')).lower()
            if any(word in content for word in keywords):
                save_news(entry)
                found = True
    if not found:
        print(f"[{datetime.now()}] Новостей не найдено.")

def run_periodically(interval_minutes=30):
    while True:
        check_feeds()
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    init_db()
    print(f"[{datetime.now()}] Инициализация завершена. Запуск цикла сбора новостей каждые 30 минут.")
    thread = threading.Thread(target=run_periodically)
    thread.daemon = True
    thread.start()

    # держим основной поток живым
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Остановка приложения.")
