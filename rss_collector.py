import sqlite3
import os
import time
import feedparser
import sys

DB_NAME = os.getenv("DB_PATH", "rss.db")

def init_db():
    """Создаём таблицы если их нет"""
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
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        c.execute('''
            INSERT OR IGNORE INTO users (username, password)
                VALUES (?, ?)
            ''', ("admin", "supersecret"))
        
        conn.commit()

def collect():
    """Ходим по лентам и собираем новости"""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        feeds = c.execute("SELECT url FROM feeds").fetchall()
        keywords = [row[0].lower() for row in c.execute("SELECT word FROM keywords").fetchall()]

        for (url,) in feeds:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                text = f"{entry.title} {entry.get('summary', '')}".lower()
                if not keywords or any(word in text for word in keywords):
                    try:
                        c.execute('''
                            INSERT INTO news (title, summary, link, published)
                            VALUES (?, ?, ?, ?)
                        ''', (
                            entry.title,
                            entry.get("summary", ""),
                            entry.link,
                            entry.get("published", "")
                        ))
                        print(f"[+] Добавлена новость: {entry.title}")
                    except sqlite3.IntegrityError:
                        # новость уже есть
                        pass
        conn.commit()

if __name__ == "__main__":
    init_db()
    if "--init-only" in sys.argv:
        sys.exit(0)
    while True:
        collect()
        print("Ждём 5 минут...")
        time.sleep(300)
