from flask import Flask, request, render_template_string, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")  # для сессий
DB_NAME = "rss.db"

HTML_LOGIN = """
<h2>Вход</h2>
<form method="POST" action="/login">
  Логин: <input name="username"><br>
  Пароль: <input type="password" name="password"><br>
  <button type="submit">Войти</button>
</form>
"""

HTML_MAIN = """
<h2>Управление</h2>
<form method="POST" action="/add_feed">
    Добавить RSS: <input name="url"><button type="submit">Добавить</button>
</form>
<form method="POST" action="/add_keyword">
    Добавить ключевое слово: <input name="word"><button type="submit">Добавить</button>
</form>
<h1>Новости</h1>
{% for n in news %}
    <div>
        <h3><a href="{{ n[3] }}">{{ n[1] }}</a></h3>
        <p>{{ n[2] }}</p>
        <small>{{ n[4] }}</small>
    </div>
{% endfor %}
<hr>
<a href="/logout">Выйти</a>
"""

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    with sqlite3.connect(DB_NAME) as conn:
        news = conn.execute("SELECT * FROM news ORDER BY published DESC LIMIT 20").fetchall()
    return render_template_string(HTML_MAIN, news=news)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return HTML_LOGIN
    username = request.form["username"]
    password = request.form["password"]
    with sqlite3.connect(DB_NAME) as conn:
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        if user:
            session["user"] = username
            return redirect("/")
    return "Неверный логин или пароль", 403

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")
