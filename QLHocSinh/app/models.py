from math import fsum

from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, logout_user, current_user
from sqlalchemy.orm import relationship, backref, column_property
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Text, Float, Enum
from werkzeug.utils import redirect
from app import db, admin
import enum


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def __str__(self):
        return self.name


# Để sử dụng @roles_required
# các role
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Bảng trung gian
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    classes = relationship('Class', backref='grade', lazy=True)

    def __str__(self):
        return self.name


class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    grade_id = Column(Integer, ForeignKey(Grade.id, ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.name


class Student(db.Model):
    __tablename__ = "student"
    # Thông tin cơ bản
    id = Column(Integer, primary_key=True)
    name = Column(Text(50), nullable=False)
    sex = Column(Text(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)

    # Khóa ngoại
    class_id = Column(Integer, ForeignKey(Class.id, ondelete="CASCADE"), nullable=False)

    def __str__(self):
        return self.name


# Môn học
class Subject(db.Model):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(Text(100), nullable=False)
    result = relationship('Result', backref='subject', lazy=True)

    def __str__(self):
        return self.name


# class student_subject(db.Model):
#     __tablename__ = 'subject_student'
#     student_id = Column(Integer, ForeignKey(Student.id), primary_key=True)
#     subject_id = Column(Integer, ForeignKey(Subject.id), primary_key=True)


# Học kì
class Semester(enum.Enum):
    first = 1
    second = 0


# Bảng điểm môn học
class Result(db.Model):
    __tablename__ = "result"
    id = Column(Integer, primary_key=True)
    semester = Column(Enum(Semester))
    fifteen = Column(Float, nullable=False)
    one_period = Column(Float, nullable=False)
    final = Column(Float, nullable=False)

    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete='CASCADE'))

    def __str__(self):
        return self.name


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class ClassView(AuthenticatedModelView):
    create_modal = True
    edit_modal = True


class StudentView(AuthenticatedModelView):
    column_list = ('id', 'name', 'sex', 'date_of_birth', 'email', 'address', 'class_id')
    column_default_sort = 'name'
    create_modal = True
    edit_modal = True


class GradeView(AuthenticatedModelView):
    column_exclude_list = 'class'
    create_modal = True
    edit_modal = True


class RolesView(AuthenticatedModelView):
    create_modal = True
    edit_modal = True


class UsersView(AuthenticatedModelView):
    create_modal = True
    edit_modal = True
    column_list = ('id', 'name', 'active', 'username')


class ResultView(AuthenticatedModelView):
    pass


class SubjectView(AuthenticatedModelView):
    pass


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


admin.add_view(UsersView(User, db.session))
admin.add_view(GradeView(Grade, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))
admin.add_view(RolesView(Role, db.session))
admin.add_view(ResultView(Result, db.session))
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(LogOutView(name='Log out'))

if __name__ == "__main__":
    db.create_all()
