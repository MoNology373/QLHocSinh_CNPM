from flask import render_template, flash, session
from flask_login import login_user, login_required, current_user
from app import app, login, dao
from app.models import *


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@login.user_loader
def user_load(user_id):
    return AdminAll.query.get(user_id)


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


# @app.route('/login-admin', methods=['POST', 'GET'])
# def login_admin():
#     if request.method == 'POST':
#         username = request.form.get("username")
#         password = request.form.get("password", "")
#
#         if adm:
#             login_user(user=adm)
#         else:
#             flash("Wrong password or account type")
#     return redirect('/admin')


@app.route('/login', methods=['GET', 'POST'])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        teach = dao.validate_user_teacher(username=username, password=password)
        adm = dao.validate_user_admin(username=username, password=password)
        if teach:
            login_user(user=teach)
            return render_template('index.html')
        else:
            if adm:
                login_user(user=adm)
                # import pdb
                # pdb.set_trace()
                flash('Thành công')
                return redirect("admin")
            else:
                flash('Thất bại')
    return render_template("login.html", err_msg=err_msg)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template("login.html")


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
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
