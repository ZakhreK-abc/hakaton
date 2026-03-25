# frontend/web/app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"   # для сессий

API_BASE_URL = "http://127.0.0.1:8000"   # адрес твоего FastAPI сервера


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]

        response = requests.post(f"{API_BASE_URL}/api/user/login", json={
            "mail": mail,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            session["user_id"] = data["user_id"]
            session["nickname"] = data["nickname"]
            flash("Успешный вход!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Неверный email или пароль", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nickname = request.form["nickname"]
        mail = request.form["mail"]
        password = request.form["password"]

        response = requests.post(f"{API_BASE_URL}/api/user/", json={
            "nickname": nickname,
            "mail": mail,
            "password": password
        })

        if response.status_code in (200, 201):
            flash("Аккаунт успешно создан! Теперь войдите.", "success")
            return redirect(url_for("login"))
        else:
            error = response.json().get("detail", "Неизвестная ошибка")
            flash(f"Ошибка: {error}", "danger")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Получаем подписки (для популярных карточек)
    subs_response = requests.get(f"{API_BASE_URL}/api/subscribe/")
    subscriptions = subs_response.json() if subs_response.status_code == 200 else []

    return render_template("dashboard.html", 
                           nickname=session["nickname"], 
                           subscriptions=subscriptions)


# ==================== НОВЫЕ ЭНДПОИНТЫ ====================

@app.route("/analytics")
def analytics():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    
    # Пример: получаем годовую статистику расходов
    try:
        resp = requests.get(f"{API_BASE_URL}/api/analytics/yearly-spending?user_id={user_id}")
        yearly_data = resp.json() if resp.status_code == 200 else {}
    except:
        yearly_data = {}

    return render_template("analytics.html", yearly_data=yearly_data)


@app.route("/my_subscriptions")
def my_subscriptions():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]
    
    # Здесь в будущем можно добавить эндпоинт /api/user/{user_id}/subscriptions
    # Пока просто заглушка
    return render_template("my_subscriptions.html")


@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("settings.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Вы успешно вышли из аккаунта", "info")
    return redirect(url_for("login"))


# ==================== DEV ЭНДПОИНТЫ ====================

@app.route("/api/dev/generate-fake-transaction", methods=["POST"])
def generate_fake_transaction():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = request.args.get("user_id", 1)
    subscribe_id = request.args.get("subscribe_id", 1)

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/dev/generate-fake-transaction?user_id={user_id}&subscribe_id={subscribe_id}"
        )
        
        if response.status_code == 200:
            data = response.json()
            flash(f"Транзакция №{data.get('transaction_id')} успешно создана!", "success")
            return {"transaction_id": data.get("transaction_id")}, 200
        else:
            flash("Ошибка при создании фейковой транзакции", "danger")
    except:
        flash("Не удалось подключиться к API", "danger")
    
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)