from flask import render_template, flash, session
from flask_login import login_user, login_required, current_user
from app import app, login, dao
from app.models import *


@app.route('/')
@login_required
def index():
    studentList = Student.query.filter().all()
    classList = Class.query.filter().all
    return render_template("index.html", studentList=studentList, classList=classList)


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = dao.validate_user_admin(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect("admin")
    return render_template("login.html", err_msg=err_msg)


@app.route('/login-teacher', methods=['GET', 'POST'])
def login_teacher():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = dao.validate_user_teacher(username=username, password=password)
        if user:
            login_user(user=user)
            flash('Thành công')
            return redirect(url_for("index"))
    return render_template("login.html", err_msg=err_msg)


# @app.route('/submit')
# @login_required
# def submit():
#     return render_template("submit.html")
#
#
@app.route('/product')
@login_required
def product():
    return render_template("product.html")


@app.route('/score')
@login_required
def score():
    return render_template("score.html")


@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
