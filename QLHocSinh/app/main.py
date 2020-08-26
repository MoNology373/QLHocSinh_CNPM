import hashlib
from functools import wraps

from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required

from app import app, login
from app.models import *


# def login_required(f):
#     @wraps(f)
#     def check(*args, **kwargs):
#         if not session.get('user'):
#             return redirect(url_for("login", next=request.url))
#         return f(*args, **kwargs)
#
#     return check


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def unauthorized_admin():
    print ('unauthorized')
    flash("You must be logged in.")
    return redirect(url_for("login_admin"))


@app.route('/login-admin', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.admin == 1,
                                 User.username == username.strip(),
                                 User.password == password.strip()).first()
        if user:
            login_user(user=user)
        else:
            flash("Wrong account or password .")
    return redirect("/admin")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('name')
#         password = request.form.get('password', '')
#         user = User.query.filter(User.username == username.strip(),
#                                  User.password == password).first()
#         if user:
#             login_user(user=user)
#         else:
#             flash("Wrong password or account.")
#     return redirect(url_for('index'))


@app.route('/submit')
@login_required
def submit():
    return render_template("submit.html")


@app.route('/product')
@login_required
def product():
    return render_template("product.html")


@app.route('/score')
@login_required
def score():
    return render_template("score.html")



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_admin'))


@app.route("/login-failed", methods=['post', 'get'])
def login_failed():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
