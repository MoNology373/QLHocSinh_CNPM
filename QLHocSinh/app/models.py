from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, logout_user, current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Text, Float
from sqlalchemy.orm import relationship, backref, column_property
from werkzeug.utils import redirect
from app import db, admin


# Người dùng nói chung
class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    fullName = column_property(lastName + ' ' + firstName)
    passWord = Column(String(500), nullable=False)
    teacher = relationship('Teacher', backref='account_teacher', uselist=False, lazy=True)
    admin = relationship('AdminAll', backref='account_admin', uselist=False, lazy=True)
    admin_check = Column(Integer, default=0)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.userName


# Giáo viên
class Teacher(db.Model):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey(User.id))
    active = Column(Boolean, default=True)
    # Nối tới class_teacher
    classes = relationship('Class', secondary='class_teacher', lazy='subquery', backref=backref('teachers', lazy=True))

    def get_id(self):
        return self.get_id()


# Admin
class AdminAll(db.Model):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey(User.id))
    # Quản lí Khối
    grades = relationship('Grade', backref='admin in charge', lazy=True)
    rules = relationship('Rule', backref='admin created', lazy=True)
    #

    def get_id(self):
        return self.id


#Khối
class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    # Có lớp
    classes = relationship('Class', backref='grade', lazy=True)
    # Thuộc Admin
    admin_id = Column(Integer, ForeignKey(AdminAll.id, ondelete='CASCADE'))

    def __str__(self):
        return self.name


class Class(db.Model):
    __tablename__ = "class"
    class_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    # Thuộc Khối
    grade_id = Column(Integer, ForeignKey(Grade.id, ondelete="CASCADE"))
    # Có Học Sinh
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.name


class Student(db.Model):
    __tablename__ = "student"
    # Thông tin cơ bản
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, unique=True, nullable=False)
    lastName = Column(Text(50), nullable=False)
    firstName = Column(Text(10), nullable=False)
    fullName = column_property(lastName + ' ' + firstName)
    gender = Column(Text(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    # Thuộc Lớp
    class_id = Column(Integer, ForeignKey(Class.class_id, ondelete="CASCADE"))
    # class_name = Column(String(50), ForeignKey(Class.name, ondelete="CASCADE"))
    # Có bảng điểm
    scores = relationship('Score', backref='student', lazy=True)

    def __str__(self):
        return self.fullName


class Subject(db.Model):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, unique=True, nullable=False)
    subject_name = Column(String(50), nullable=False)
    # Có bảng điểm
    scores = relationship('Score', backref='subject', lazy=True)

    def __str__(self):
        return self.subject_name


#
class Semester(db.Model):
    __tablename__ = 'semester'
    id = Column(Integer, primary_key=True, autoincrement=True)
    semester_id = Column(Integer, unique=True, nullable=False)
    semester_name = Column(Integer)
    # Có bảng điểm
    scores = relationship('Score', backref='semester', lazy=True)


class Score(db.Model):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    score_id = Column(Integer, unique=True, nullable=False)
    score_fifteen = Column(Float, default=0)
    score_period = Column(Float, default=0)
    score_final = Column(Float, default=0)
    # Thuộc Môn học
    subject_id = Column(Integer, ForeignKey(Subject.id, ondelete='CASCADE'))
    # Thuộc Học sinh
    student_id = Column(Integer, ForeignKey(Student.student_id, ondelete='CASCADE'))
    # Thuộc Học kì
    semester_id = Column(Integer, ForeignKey(Semester.id, ondelete='CASCADE'))


#
#
class_teacher = db.Table('class_teacher',
                         Column('class_id', Integer,
                                ForeignKey(Class.class_id),
                                primary_key=True),
                         Column('teacher_name', Integer,
                                ForeignKey(Teacher.id),
                                primary_key=True))


class Rule(db.Model):
    __tablename__="rule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(50))
    content = Column(String(500), nullable=False)
    admin_id = Column(Integer, ForeignKey(AdminAll.id, ondelete='CASCADE'))


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin_check == 1

    create_modal = True
    can_view_details = True
    column_display_all_relations = True
    can_set_page_size = True
    column_auto_select_related = True


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('/login', next=request.url))


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


class ToTeacherView(AuthenticatedBaseView):
    @expose('/')
    def to_admin(self):
        return redirect('/')


class TeacherView(AuthenticatedModelView):
    pass


class AdminView(AuthenticatedModelView):
    column_display_all_relations = False
    can_create = False
    can_edit = True
    can_delete = False


class GradeView(AuthenticatedModelView):
    pass


class ClassView(AuthenticatedModelView):
    pass


class StudentView(AuthenticatedModelView):
    column_labels = dict(fullName='Full name', student_id='Student ID', lastName='Last name', firstName='First name')
    column_searchable_list = ['fullName', 'student_id', 'lastName', 'firstName', Class.name]
    column_display_all_relations = False


class ScoreView(AuthenticatedModelView):
    column_searchable_list = [Subject.subject_name]


class SubjectView(AuthenticatedModelView):
    column_display_all_relations = False


class SemesterView(AuthenticatedModelView):
    column_display_all_relations = False


class UserView(AuthenticatedModelView):
    column_display_all_relations = False
    column_exclude_list = 'passWord'


class RuleView(AuthenticatedModelView):
    pass


admin.add_view(UserView(User, db.session, category="Users"))
admin.add_view(TeacherView(Teacher, db.session, category="Users"))
admin.add_view(AdminView(AdminAll, db.session, category="Users"))
#
admin.add_view(GradeView(Grade, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))

admin.add_view(SubjectView(Subject, db.session))
admin.add_view(SemesterView(Semester, db.session))
admin.add_view(ScoreView(Score, db.session))
admin.add_view(RuleView(Rule, db.session))
admin.add_view(LogOutView(name='Log out'))
admin.add_view(ToTeacherView(name='To teacher view'))
if __name__ == "__main__":
    db.create_all()
