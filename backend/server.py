from flask import Flask, request, render_template
import json




app = Flask(__name__)


@app.get("/")
def home():
    return render_template("web.html")

@app.post('/login')
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    with open("users.json", 'r') as users_data:
        data = json.load(users_data)
        for user in data:
            if username == user["username"] and password == user["password"]:
                return "<p>Hello, World!</p>"
    users_data.close()
    return render_template("web.html")