from functools import wraps
from flask import render_template, session, request, url_for

from werkzeug.utils import redirect
from app import app
from app.models import *

def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if not session.get('user'):
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return check


@app.route('/')
# @login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # err_msg = ""
    # if request.method == 'POST':
    #     username = request.form.get('name')
    #     password = request.form.get('password')
    #         return redirect(url_for('index')
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    session["user"] = None
    return redirect(url_for('login'))


@app.route("/login-failed", methods=['post', 'get'])
def login_failed():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
