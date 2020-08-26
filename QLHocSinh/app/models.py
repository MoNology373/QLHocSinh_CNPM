from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, logout_user, current_user
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from werkzeug.utils import redirect
from app import db, admin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    admin = Column(String(50), nullable=False)
    def __str__(self):
        return self.name


class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.name


class Student(db.Model):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)

    def __str__(self):
        return self.name


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ClassView(AuthenticatedModelView):
    pass


class StudentView(AuthenticatedModelView):
    pass


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))
admin.add_view(LogOutView(name='Log out'))

if __name__ == "__main__":
    db.create_all()
