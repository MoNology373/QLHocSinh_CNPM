import string
from datetime import timedelta

from flask import render_template, session, request, url_for
# from flask_login import LoginManager, login_user, login_required
# from flask_wtf import FlaskForm
from werkzeug.utils import redirect

from app import app, dao

# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, Config
# from wtforms import StringField, PasswordField, SubmitField
# from PY2 import ._compat, text_type

#
# @app.route("/")
# def index():
#     return render_template("submit.html")
#
#
# @app.route("/products")
# def product_load():
#     return render_template("product.html", products=dao.read_products())
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "guhgy vgr137y 13 [][][2yrgy1g"
app.permanent_session_lifetime = timedelta(minutes = 5)
# app.config.from_object(Config)
# login_manager = LoginManager()
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login_manager.init_app(app)


# class User(object):
#     '''
#         This provides default implementations for the methods that Flask-Login
#         expects user objects to have.
#         '''
#
#     if not PY2:  # pragma: no cover
#         # Python 3 implicitly set __hash__ to None if we override __eq__
#         # We set it back to its default implementation
#         __hash__ = object.__hash__
#
#     @property
#     def is_active(self):
#         return True
#
#     @property
#     def is_authenticated(self):
#         return True
#
#     @property
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         try:
#             return text_type(self.id)
#         except AttributeError:
#             raise NotImplementedError('No `id` attribute - override `get_id`')
#
#     def __eq__(self, other):
#         '''
#         Checks the equality of two `UserMixin` objects using `get_id`.
#         '''
#         if isinstance(other, UserMixin):
#             return self.get_id() == other.get_id()
#         return NotImplemented
#
#     def __ne__(self, other):
#         '''
#         Checks the inequality of two `UserMixin` objects using `get_id`.
#         '''
#         equal = self.__eq__(other)
#         if equal is NotImplemented:
#             return NotImplemented
#         return not equal


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

@app.route("/index")
# @login_required
def index():
    return render_template("index.html")


@app.route('/')
def user():
    if 'username' in session and 'password' in session:
        return redirect(url_for("index", name =session['username']))
    else:
        return redirect(url_for('login'))


# class LoginForm(FlaskForm):
#     username = StringField('Username')
#     password = PasswordField('Password')
#     submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' and 'password' in session:
        return redirect(url_for('user'))
    else:
        if request.method == 'POST':
            session['username'] = request.form['email']
            session['password'] = request.form['password']
            if session['username'] == "admin@gmail" and session['password'] == "123":
                return redirect(url_for('index', name=session['username']))
            else:
                session.pop('username', None)
                session.pop('password', None)
                return redirect(url_for("loginfailed", name="idiot"))
        return render_template("login.html")


@app.route("/products")
def product_load():
    if 'username' and 'password' in session:
        return render_template("product.html", products=dao.read_products())
    else:
        return redirect(url_for('login'))

@app.route("/scores")
def score_load():
    if 'username' and 'password' in session:
        return render_template("score.html", scores=dao.read_products())
    else:
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login'))


@app.route("/login-failed", methods=['post', 'get'])
def loginfailed():
    if request.method == 'POST':
        session['username'] = request.form['email']
        session['password'] = request.form['password']
        if session['username'] == "admin@gmail" and session['password'] == "123":
            return redirect(url_for('index', name=session['username']))
        else:
            return redirect(url_for("loginfailed", name="idiot"))
    return render_template("login.html")

if __name__ == "__main__":
    app.run()