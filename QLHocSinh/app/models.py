from datetime import datetime
import flask_admin_subview
from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, logout_user, current_user
from flask_security import RoleMixin
from sqlalchemy.orm import relationship, backref, column_property
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Text, Float
from werkzeug.utils import redirect
from app import db, admin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(500), nullable=False)
    # password = sha256((Column(String(500), nullable=False)).encode('utf-8')).hexdigest()
    roles = db.relationship('Role', secondary='user_roles', backref=backref('users', lazy='dynamic'))

    def __str__(self):
        return self.name


# Để sử dụng @roles_required
# các role
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Bảng trung gian
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Khối
class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)

    classes = relationship('Class', backref='grade', lazy=True)
    students = relationship('Student', backref='grade', lazy=True)

    def __str__(self):
        return self.name


class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True, unique=True)
    grade_id = Column(Integer, ForeignKey(Grade.id, ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    students = relationship('Student', backref='class', lazy=True)
    # students = relationship('Student', lazy=True)

    def __str__(self):
        return self.name


# Học kì
class SemesterOne(db.Model):
    __tablename__ = "semester_one"
    id = Column(Integer, primary_key=True, unique=True)
    # Khóa ngoại tới bảng reuslt
    result = relationship('Result', back_populates='semester_one', uselist=False)
    # Khóa ngoại chứa hình thức kiểm tra
    test_type = relationship('TestType', backref=backref('semester_one', uselist=False))
    test_type_id = Column(Integer, ForeignKey('test_type.id'))


class SemesterTwo(db.Model):
    __tablename__ = "semester_two"
    id = Column(Integer, primary_key=True, unique=True)
    # Khóa ngoại tới bảng result
    result = relationship('Result', back_populates='semester_two', uselist=False)
    # Khóa ngoại chứa hình thức kiểm tra
    test_type = relationship('TestType', backref=backref('semester_two', uselist=False))
    test_type_id = Column(Integer, ForeignKey('test_type.id'))


# Bảng điểm môn học
class Result(db.Model):
    __tablename__ = "result"
    id = Column(Integer, primary_key=True, unique=True)
    # Khóa ngoại
    student = relationship('Student', back_populates='result', uselist=False)
    # Bảng điểm chứa các id của các học kì
    semester_one = relationship('SemesterOne', backref=backref('result_one', uselist=False))
    semester_one_id = Column(Integer, ForeignKey(SemesterOne.id))
    semester_two = relationship('SemesterTwo', backref=backref('result_two', uselist=False))
    semester_two_id = Column(Integer, ForeignKey(SemesterTwo.id))


# def validate_form(form):
#     if form.date_of_birth - datetime.today() < 0:


class Student(db.Model):
    __tablename__ = "student"
    # Thông tin cơ bản
    student_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(Text(50), nullable=False)
    sex = Column(Text(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    # Khóa ngoại
    grade_id = Column(Integer, ForeignKey(Grade.id, ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id, ondelete="CASCADE"), nullable=False)

    result_id = Column(Integer, ForeignKey(Result.id))
    result = relationship('Result', uselist=False, back_populates='student')

    def __str__(self):
        return self.name


class TestType(db.Model):
    __tablename__ = "test_type"
    id = Column(Integer, primary_key=True, unique=True)
    # Điểm 15'
    subject_fifteen_id = Column(Integer, ForeignKey('subject_fifteen.id'))
    subject_fifteen = relationship('SubjectFifteen', back_populates='test_type')
    # Điểm 1 tiết
    subject_period_id = Column(Integer, ForeignKey('subject_period.id'))
    subject_period = relationship('SubjectPeriod', back_populates='test_type')
    # Điểu cuối kì
    subject_final_id = Column(Integer, ForeignKey('subject_final.id'))
    subject_final = relationship('SubjectFinal', back_populates='test_type')

    def __str__(self):
        return self.name


class SubjectFifteen(db.Model):
    __tablename__ = "subject_fifteen"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại
    test_type = relationship('TestType', back_populates='subject_fifteen', uselist=False)


class SubjectPeriod(db.Model):
    __tablename__ = "subject_period"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại
    test_type = relationship('TestType', back_populates='subject_period', uselist=False)


class SubjectFinal(db.Model):
    __tablename__ = "subject_final"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại
    test_type = relationship('TestType', back_populates='subject_final', uselist=False)


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
    column_display_pk = True
    # form_columns = ('student_id', 'name', 'sex', 'date_of_birth', 'email', 'address', 'grade_id', 'class_id', 'result_id')
    column_default_sort = 'student_id'
    column_searchable_list = ['name', 'student_id']
    create_modal = True
    edit_modal = True


class GradeView(AuthenticatedModelView):
    column_exclude_list = 'Class'
    column_display_pk = True
    create_modal = True
    edit_modal = True


class RolesView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class UsersView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = ('id', 'name', 'active', 'username', 'role_id')


class SemesterOneView(AuthenticatedModelView):
    column_list = ('id', 'subject_fifteen', 'subject_period', 'subject_final')
    column_display_pk = True
    create_modal = True
    edit_modal = True


class SemesterTwoView(AuthenticatedModelView):
    column_list = ('id', 'subject_fifteen', 'subject_period', 'subject_final')
    column_display_pk = True
    create_modal = True
    edit_modal = True


class TestTypeView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class SubjectFifteenView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class SubjectPeriodView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class SubjectFinalView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class ResultView(AuthenticatedModelView):
    form_columns = ('id', 'semester_one_id', 'semester_two_id')
    create_modal = True
    edit_modal = True
    column_display_pk = True
    column_list = ('id', 'semester_one_id', 'semester_two_id')
    pass


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


admin.add_view(UsersView(User, db.session))
admin.add_view(RolesView(Role, db.session))

admin.add_view(GradeView(Grade, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))

admin.add_view(ResultView(Result, db.session))
# admin.ad
admin.add_view(SemesterOneView(SemesterOne, db.session, category='Semesters'))
admin.add_view(SemesterTwoView(SemesterTwo, db.session, category='Semesters'))
# admin.add_view(SemesterOneView(SemesterOne, db.session), category="Semesters")
# admin.add_view(SemesterTwoView(SemesterTwo, db.session), category="Semesters")
# admin.add_view(TestTypeView(TestType, db.session))

admin.add_view(SubjectFifteenView(SubjectFifteen, db.session, category='Score'))
admin.add_view(SubjectPeriodView(SubjectPeriod, db.session, category='Score'))
admin.add_view(SubjectFinalView(SubjectFinal, db.session, category='Score'))

admin.add_view(LogOutView(name='Log out'))

if __name__ == "__main__":
    db.create_all()
