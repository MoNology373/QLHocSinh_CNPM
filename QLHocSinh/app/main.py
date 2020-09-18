from flask import render_template, flash, session
from flask_login import login_user, login_required, current_user
from app import app, login, dao
from app.models import *


@app.route('/')
@login_required
def index():
    # studentList = Student.query.filter().all()
    studentList = Student.query.join(Class, Student.class_id == Class.class_id).add_columns(Student.student_id,
                                                                                            Student.lastName,
                                                                                            Student.firstName,
                                                                                            Student.gender,
                                                                                            Student.date_of_birth,
                                                                                            Student.email,
                                                                                            Student.address,
                                                                                            Class.name)
    # classList = Class.query.filter().all
    return render_template("index.html", studentList=studentList)


@app.route('/score-semester-1')
@login_required
def score_semester_1():
    # Student: student_id, lastName, firstName
    # Subject: subject_name
    # Semester: semester_name
    # Score: score_fifteen, score_period, score_final
    # Class: name
    # studentList = Student.query.join(Class, Student.class_id == Class.class_id) \
    #     .add_columns(Student.student_id, Student.lastName, Student.firstName, Class.name)

    scoreList = Score.query.join(Student).join(Class).join(Semester).join(Subject)\
        .add_columns(Student.student_id, Student.lastName, Student.firstName,
                     Class.name, Semester.semester_name, Subject.subject_name,
                     Score.score_fifteen, Score.score_period, Score.score_final).filter(Semester.semester_name == "1")

    # scoreListBySemester = Semester.query.join(scoreList, Semester.semester_id == Score.semester_id) \
    #     .add_columns(Student.student_id, Student.lastName, Student.firstName, Semester.semester_name,
    #                  Score.score_fifteen, Score.score_period, Score.score_final, Class.name)
    # scoreListBySubject = Subject.query.join(scoreListBySemester, Subject.id == Score.subject_id) \
    #     .add_column(Student.student_id, Student.lastName, Student.firstName, Semester.semester_name,
    #                 Subject.subject_name,
    #                 Score.score_fifteen, Score.score_period, Score.score_final, Class.name)
    return render_template("score-semester-1.html", scoreList=scoreList)


@app.route('/score-semester-2')
@login_required
def score_semester_2():
    # Student: student_id, lastName, firstName
    # Subject: subject_name
    # Semester: semester_name
    # Score: score_fifteen, score_period, score_final
    # Class: name
    # studentList = Student.query.join(Class, Student.class_id == Class.class_id) \
    #     .add_columns(Student.student_id, Student.lastName, Student.firstName, Class.name)

    scoreList = Score.query.join(Student).join(Class).join(Semester).join(Subject)\
        .add_columns(Student.student_id, Student.lastName, Student.firstName,
                     Class.name, Semester.semester_name, Subject.subject_name,
                     Score.score_fifteen, Score.score_period, Score.score_final).filter(Semester.semester_name == "2")

    # scoreListBySemester = Semester.query.join(scoreList, Semester.semester_id == Score.semester_id) \
    #     .add_columns(Student.student_id, Student.lastName, Student.firstName, Semester.semester_name,
    #                  Score.score_fifteen, Score.score_period, Score.score_final, Class.name)
    # scoreListBySubject = Subject.query.join(scoreListBySemester, Subject.id == Score.subject_id) \
    #     .add_column(Student.student_id, Student.lastName, Student.firstName, Semester.semester_name,
    #                 Subject.subject_name,
    #                 Score.score_fifteen, Score.score_period, Score.score_final, Class.name)
    return render_template("score-semester-2.html", scoreList=scoreList)

@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@login.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = dao.validate_user_admin(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect("admin")
    return render_template("login.html", err_msg=err_msg)


@app.route('/login-teacher', methods=['GET', 'POST'])
def login_teacher():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        user = dao.validate_user_teacher(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for("index"))
    return render_template("login.html", err_msg=err_msg)


# @app.route('/submit')
# @login_required
# def submit():
#     return render_template("submit.html")
#
#
# @app.route('/product')
# @login_required
# def product():
#     return render_template("product.html")


@app.route('/log-out')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()
