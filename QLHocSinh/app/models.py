from flask import url_for, request
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, logout_user, current_user
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, Text, Float
from sqlalchemy.orm import relationship, backref, column_property
from werkzeug.utils import redirect
from app import db, admin


# Giáo viên
class Teacher(db.Model, UserMixin):
    __tablename__ = "teacher"

    active = Column(Boolean, default=True)
    userName = Column(String(50), nullable=False, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    fullName = column_property(lastName + ' ' + firstName)
    passWord = Column(String(500), nullable=False)
    # Nối tới class_teacher
    classes = relationship('Class', secondary='class_teacher', lazy='subquery', backref=backref('teachers', lazy=True))

    def __str__(self):
        return self.userName

    def get_id(self):
        return self.userName


# Admin
class AdminAll(db.Model, UserMixin):
    __tablename__ = "admin"

    userName = Column(String(50), primary_key=True, nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    fullName = column_property(lastName + ' ' + firstName)
    passWord = Column(String(500), nullable=False)
    # Quản lí Khối
    grades = relationship('Grade', backref='admin', lazy=True)

    def get_id(self):
        return self.userName

    def __str__(self):
        return self.userName


# Khối
class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    # Có lớp
    classes = relationship('Class', backref='grade', lazy=True)
    # Thuộc Admin
    admin_id = Column(String(50), ForeignKey(AdminAll.userName, ondelete='CASCADE'))

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
    student_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    lastName = Column(Text(50), nullable=False)
    firstName = Column(Text(10), nullable=False)
    fullName = column_property(lastName + ' ' + firstName)
    gender = Column(Text(10), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    # Thuộc Lớp
    class_id = Column(Integer, ForeignKey(Class.class_id, ondelete="CASCADE"))
    # Có bảng điểm
    scores = relationship('Score', backref='student', lazy=True)

    def __str__(self):
        return self.fullName


class Subject(db.Model):
    __tablename__ = 'subject'
    subject_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    subject_name = Column(String(50), nullable=False)
    # Có bảng điểm
    scores = relationship('Score', backref='subject', lazy=True)

    def __str__(self):
        return self.subject_name


class Semester(db.Model):
    __tablename__ = 'semester'
    semester_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    semester_name = Column(Integer)
    # Có bảng điểm
    scores = relationship('Score', backref='semester', lazy=True)

    def __str__(self):
        return self.semester_name


class Score(db.Model):
    __tablename__ = 'score'
    score_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    score_fifteen = Column(Float, default=0)
    score_period = Column(Float, default=0)
    score_final = Column(Float, default=0)
    # Thuộc Môn học
    subject_id = Column(Integer, ForeignKey(Subject.subject_id, ondelete='CASCADE'))
    # Thuộc Học sinh
    student_id = Column(Integer, ForeignKey(Student.student_id, ondelete='CASCADE'))
    # Thuộc Học kì
    semester_id = Column(Integer, ForeignKey(Semester.semester_id, ondelete='CASCADE'))


class_teacher = db.Table('class_teacher',
                         Column('class_id', Integer,
                                ForeignKey(Class.class_id),
                                primary_key=True),
                         Column('teacher_name', String(50),
                                ForeignKey(Teacher.userName),
                                primary_key=True))


#
#
#
#
#
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    can_view_details = True
    column_display_all_relations = True
    can_set_page_size = True
    column_auto_select_related = True


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('/login', next=request.url))


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


class TeacherView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True


class AdminView(AuthenticatedModelView):
    can_create = False
    can_edit = True
    can_delete = False
    create_modal = True
    column_display_pk = True


class GradeView(AuthenticatedModelView):
    # form_columns = ('id', 'name', 'admin_id')
    # column_list = ('id', 'name', 'admin_id')
    create_modal = True
    column_display_pk = True


class ClassView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True


class StudentView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True
    column_searchable_list = ["fullName", "student_id", "class_id"]
    # column_labels = dict()


class ScoreView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True


class SubjectView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True


class SemesterView(AuthenticatedModelView):
    create_modal = True
    column_display_pk = True


admin.add_view(TeacherView(Teacher, db.session))
admin.add_view(AdminView(AdminAll, db.session))
#
admin.add_view(GradeView(Grade, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))
#
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(SemesterView(Semester, db.session))
admin.add_view(ScoreView(Score, db.session))


admin.add_view(LogOutView(name='Log out'))

if __name__ == "__main__":
    db.create_all()
