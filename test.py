import json
import logging
import os
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, flash

GROUP_SEED = 322356551 ^ 111111111
HASHING_MODE = "None"
PROTACTION_FLAGS = "None"
latency_ms = 0

app = Flask(__name__)

USER_DATA_FILE = 'users.json'
LOG_FILE = 'attempts.log'


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_user_data():

    if not os.path.exists(USER_DATA_FILE):
        logging.error(f"User data file not found: {USER_DATA_FILE}")
        return {}
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Unexpected error loading user data: {e}")
        return {}

def authenticate_user(username, password):
    users = load_user_data()
    for user in users:
        if username == user["username"] and password == user["password"]:
            return True
    
    return False

def log_login_attempt(username, status):
    log_message = f"Login Attempt | User: {username} | result: {status} | latency ms: {latency_ms} |\
    hash mode: {HASHING_MODE} | protection flags: {PROTACTION_FLAGS} | group seed: {GROUP_SEED} "
    logging.info(log_message)



@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        log_login_attempt('N/A (Missing fields)', 'FAILED')
        return render_template('login.html', error_message="Authentication failed, missing data")

    if authenticate_user(username, password):
        log_login_attempt(username, 'SUCCESS')
        return render_template('login.html', success_message="Authentication Successful!")
    else:
        log_login_attempt(username, 'FAILURE')
        return render_template('login.html', error_message="Authentication failed!")

if __name__ == '__main__':
    app.run()