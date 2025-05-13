from flask import Flask, request, render_template_string, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = "rss.db"

HTML = """
<h1>Новости</h1>
{% for n in news %}
    <div>
        <h3><a href="{{ n[3] }}">{{ n[1] }}</a></h3>
        <p>{{ n[2] }}</p>
        <small>{{ n[4] }}</small>
    </div>
{% endfor %}
<hr>
<h2>Управление</h2>
<form method="POST" action="/add_feed">
    Добавить RSS: <input name="url"><button type="submit">Добавить</button>
</form>
<form method="POST" action="/add_keyword">
    Добавить ключевое слово: <input name="word"><button type="submit">Добавить</button>
</form>
"""

@app.route("/")
def index():
    with sqlite3.connect(DB_NAME) as conn:
        news = conn.execute("SELECT * FROM news ORDER BY published DESC LIMIT 20").fetchall()
    return render_template_string(HTML, news=news)

@app.route("/add_feed", methods=["POST"])
def add_feed():
    url = request.form["url"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT OR IGNORE INTO feeds (url) VALUES (?)", (url,))
        conn.commit()
    return redirect("/")

@app.route("/add_keyword", methods=["POST"])
def add_keyword():
    word = request.form["word"]
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT OR IGNORE INTO keywords (word) VALUES (?)", (word,))
        conn.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True,port=5000, host='0.0.0.0')

