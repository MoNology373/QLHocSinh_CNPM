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
    fullName = column_property(firstName + ' ' + lastName)
    passWord = Column(String(500), nullable=False)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.userName


# Admin
class AdminAll(db.Model, UserMixin):
    __tablename__ = "admin"

    userName = Column(String(50), primary_key=True, nullable=False)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    fullName = column_property(firstName + ' ' + lastName)
    passWord = Column(String(500), nullable=False)

    def get_id(self):
        return self.userName


# Khối
class Grade(db.Model):
    __tablename__ = "grade"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)

    classes = relationship('Class', backref='grade', lazy=True)

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
    # result = relationship('Result', back_populates='semester_one', uselist=False)
    # Khóa ngoại chứa hình thức kiểm tra
    test_type_one = relationship("TestTypeOne", backref="semester_one", lazy=True)
    test_type_one_id = Column(Integer, ForeignKey('test_type_one.id'), nullable=False)


class SemesterTwo(db.Model):
    __tablename__ = "semester_two"
    id = Column(Integer, primary_key=True, unique=True)
    # Khóa ngoại tới bảng result
    # result = relationship('Result', back_populates='semester_two', uselist=False)
    # Khóa ngoại chứa hình thức kiểm tra
    test_type_two = relationship("TestTypeTwo", backref="semester_two", lazy=True)
    test_type_two_id = Column(Integer, ForeignKey('test_type_two.id'), nullable=False)


# Bảng điểm môn học
class Result(db.Model):
    __tablename__ = "result"
    id = Column(Integer, primary_key=True, unique=True)
    # Khóa ngoại
    student = relationship('Student', back_populates='result', uselist=False)
    # Bảng điểm chứa các id của các học kì
    semester_one = relationship('SemesterOne', backref=backref('result_one', uselist=False))
    semester_one_id = Column(Integer, ForeignKey(SemesterOne.id), nullable=False)

    semester_two = relationship('SemesterTwo', backref=backref('result_two', uselist=False))
    semester_two_id = Column(Integer, ForeignKey(SemesterTwo.id), nullable=False)


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
    class_id = Column(Integer, ForeignKey(Class.id, ondelete="CASCADE"), nullable=False)

    result_id = Column(Integer, ForeignKey(Result.id))
    result = relationship('Result', uselist=False, back_populates='student')

    def __str__(self):
        return self.name


# Các hình thức kiểm tra thuộc HK1
class TestTypeOne(db.Model):
    __tablename__ = "test_type_one"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    # Điểm 15'
    subject_fifteen_one_id = Column(Integer, ForeignKey('subject_fifteen_one.id'))
    subject_fifteen_one = relationship('SubjectFifteenOne', back_populates='test_type_one')
    # Điểm 1 tiết
    subject_period_id_one = Column(Integer, ForeignKey('subject_period_one.id'))
    subject_period_one = relationship('SubjectPeriodOne', back_populates='test_type_one')
    # Điểu cuối kì
    subject_final_one_id = Column(Integer, ForeignKey('subject_final_one.id'))
    subject_final_one = relationship('SubjectFinalOne', back_populates='test_type_one')
    # Khóa ngoại tới SemesterOne
    # semester_one_id = Column(Integer, ForeignKey(SemesterOne.id, ondelete="CASCADE"))
    # semester_one = relationship('SemesterOne', back_populates='test_type_one')

    def __str__(self):
        return self.name


# Các hình thức kiểm tra thuộc HK2
class TestTypeTwo(db.Model):
    __tablename__ = "test_type_two"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50), nullable=False)
    # Điểm 15'
    subject_fifteen_two_id = Column(Integer, ForeignKey('subject_fifteen_two.id'))
    subject_fifteen_two = relationship('SubjectFifteenTwo', back_populates='test_type_two')
    # Điểm 1 tiết
    subject_period_two_id = Column(Integer, ForeignKey('subject_period_two.id'))
    subject_period_two = relationship('SubjectPeriodTwo', back_populates='test_type_two')
    # Điểu cuối kì
    subject_final_two_id = Column(Integer, ForeignKey('subject_final_two.id'))
    subject_final_two = relationship('SubjectFinalTwo', back_populates='test_type_two')
    # Khóa ngoại tới SemesterTwo
    # semester_two_id = Column(Integer, ForeignKey(SemesterTwo.id, ondelete="CASCADE"))
    # semester_two = relationship('SemesterTwo', back_populates='test_type_two')

    def __str__(self):
        return self.name


# Học kì 1
# Các hình thức kiểm tra
class SubjectFifteenOne(db.Model):
    __tablename__ = "subject_fifteen_one"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeOne
    test_type_one = relationship('TestTypeOne', back_populates='subject_fifteen_one')
    # test_type_one_id = Column(Integer, ForeignKey(TestTypeOne.id, ondelete="CASCADE"), nullable=False)


# Các hình thức kiểm tra
class SubjectPeriodOne(db.Model):
    __tablename__ = "subject_period_one"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeOne
    test_type_one = relationship('TestTypeOne', back_populates='subject_period_one')
    # test_type_one_id = Column(Integer, ForeignKey(TestTypeOne.id, ondelete="CASCADE"), nullable=False)


# Các hình thức kiểm tra
class SubjectFinalOne(db.Model):
    __tablename__ = "subject_final_one"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeOne
    test_type_one = relationship('TestTypeOne', back_populates='subject_final_one')
    # test_type_one_id = Column(Integer, ForeignKey(TestTypeOne.id, ondelete="CASCADE"), nullable=False)


# Học kì 2
# Các hình thức kiểm tra
class SubjectFifteenTwo(db.Model):
    __tablename__ = "subject_fifteen_two"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeTwo
    test_type_two = relationship('TestTypeTwo', back_populates='subject_fifteen_two')
    # test_type_two_id = Column(Integer, ForeignKey(TestTypeTwo.id, ondelete="CASCADE"), nullable=False)


# Các hình thức kiểm tra
class SubjectPeriodTwo(db.Model):
    __tablename__ = "subject_period_two"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeTwo
    test_type_two = relationship('TestTypeTwo', back_populates='subject_period_two')
    # test_type_two_id = Column(Integer, ForeignKey(TestTypeTwo.id, ondelete="CASCADE"), nullable=False)


# Các hình thức kiểm tra
class SubjectFinalTwo(db.Model):
    __tablename__ = "subject_final_two"
    id = Column(Integer, primary_key=True, unique=True)
    math = Column(Float, default=0)
    physic = Column(Float, default=0)
    chem = Column(Float, default=0)
    bio = Column(Float, default=0)
    his = Column(Float, default=0)
    geo = Column(Float, default=0)
    pe = Column(Float, default=0)
    # Khóa ngoại tới TestTypeTwo
    test_type_two = relationship('TestTypeTwo', back_populates='subject_final_two')
    # test_type_two_id = Column(Integer, ForeignKey(TestTypeTwo.id, ondelete="CASCADE"), nullable=False)


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('/login', next=request.url))


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('/login', next=request.url))


class ClassView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class StudentView(AuthenticatedModelView):
    column_display_pk = True
    form_columns = ('student_id', 'name', 'sex', 'date_of_birth', 'email', 'address', 'class_id', 'result_id')
    # column_list = ('student_id', 'name', 'sex', 'date_of_birth', 'email', 'address', 'class_id', 'result_id')
    column_default_sort = 'student_id'
    column_searchable_list = ['name', 'student_id', 'sex', 'class_id']
    create_modal = True
    edit_modal = True


class GradeView(AuthenticatedModelView):
    column_display_pk = True
    create_modal = True
    edit_modal = True


class TeacherView(AuthenticatedModelView):
    # Có thể chỉnh sửa hoặc tạo
    form_columns = ('userName', 'active', 'firstName', 'lastName', 'passWord')
    # Thể hiện ở table
    column_list = ('fullName', 'userName', 'active', 'firstName', 'lastName')
    column_display_pk = True
    create_modal = True
    edit_modal = True


class AdminAllView(AuthenticatedModelView):
    column_list = ('fullName', 'userName', 'firstName', 'lastName')
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = False
    create_modal = True
    edit_modal = True


class SemesterOneView(AuthenticatedModelView):
    # column_list = ('id', 'test_type')
    # form_columns = ('id', 'test_type_one_id')
    # column_list = ('id', 'test_type_one_id')
    create_modal = True
    edit_modal = True


class SemesterTwoView(AuthenticatedModelView):
    # form_columns = ('id', 'test_type_two_id')
    # column_list = ('id', 'test_type_two_id')
    create_modal = True
    edit_modal = True


class TestTypeOneView(AuthenticatedModelView):
    column_list = ('id', 'name', 'subject_fifteen_one_id', 'subject_period_id_one', 'subject_final_one_id')
    column_display_pk = True
    create_modal = True
    edit_modal = True


class TestTypeTwoView(AuthenticatedModelView):
    column_list = ('id', 'subject_fifteen_two_id', 'subject_period_two_id', 'subject_final_two_id')
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
    # form_columns = ('id', 'semester_one_id', 'semester_two_id')
    column_list = ('id', 'semester one', 'semester two')
    create_modal = True
    edit_modal = True
    column_display_pk = True


class LogOutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


admin.add_view(TeacherView(Teacher, db.session))
admin.add_view(AdminAllView(AdminAll, db.session))

admin.add_view(GradeView(Grade, db.session))
admin.add_view(ClassView(Class, db.session))
admin.add_view(StudentView(Student, db.session))

admin.add_view(ResultView(Result, db.session))
admin.add_view(SemesterOneView(SemesterOne, db.session, category='Semesters'))
admin.add_view(SemesterTwoView(SemesterTwo, db.session, category='Semesters'))

admin.add_view(TestTypeOneView(TestTypeOne, db.session, category='Test Types'))
admin.add_view(TestTypeTwoView(TestTypeTwo, db.session, category='Test Types'))

admin.add_view(SubjectFifteenView(SubjectFifteenOne, db.session, category='Semester One Score'))
admin.add_view(SubjectPeriodView(SubjectPeriodOne, db.session, category='Semester One Score'))
admin.add_view(SubjectFinalView(SubjectFinalOne, db.session, category='Semester One Score'))

admin.add_view(SubjectFifteenView(SubjectFifteenTwo, db.session, category='Semester Two Score'))
admin.add_view(SubjectPeriodView(SubjectPeriodTwo, db.session, category='Semester Two Score'))
admin.add_view(SubjectFinalView(SubjectFinalTwo, db.session, category='Semester Two Score'))

admin.add_view(LogOutView(name='Log out'))

if __name__ == "__main__":
    db.create_all()
