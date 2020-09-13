import hashlib
from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required
from flask_user import roles_required
from app import app, login
from app.models import *


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def unauthorized_admin():
    print('unauthorized')
    flash("You must be logged in.")
    return redirect(url_for("login"))


@app.route('/admin')
@roles_required('Admin')
def admin():
    render_template('admin/index.html')


@app.route('/login-admin', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password.strip()).first()
        # User.query.join(Role.users).filter(role_id == 1).all()).first()
        if user:
            role = User.query.join(User.roles).filter(User.id == user.get_id()).first()
            if role:
                login_user(user=user)
            elif User.active == 1:
                flash("Account is inactive.")
            else:
                flash("Wrong account type.")
        else:
            flash("Wrong password.")
    return redirect("/admin")


@app.route('/login-teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password.strip()).first()
        if user:
            login_user(user=user)
        else:
            flash("Wrong password.")
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/submit')
@roles_required('Admin')
@login_required
def submit():
    return render_template("submit.html")


@app.route('/product')
@roles_required('Admin')
@login_required
def product():
    return render_template("product.html")


@app.route('/score')
@roles_required('Admin')
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
