from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_admin_subview import Subview

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:namlun218@localhost/studentmanagementdb?charset=utf8mb4"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost/studentmanagementdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.secret_key = "vji  fuehf uhroih uo31hro31yr3yro31e3y r oryog"

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUAN LY HOC SINH", template_mode="bootstrap3")

login = LoginManager(app=app)

Subview(app, template_mode="bootstrap3")

