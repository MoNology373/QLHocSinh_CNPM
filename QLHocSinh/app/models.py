from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import render_template
from app import db, admin



# class User(db.Model, UserMixin):
#     __tablename__ = "user"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)
#     password = Column(String(500), nullable=False)

class Class(db.Model):
    __tablename__ = "class"
    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    students = relationship('Student', backref='class', lazy=True)

    def __str__(self):
        return self.name

class Student(db.Model):
    __tablename__="student"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)

    def __str__(self):
        return self.name


admin.add_view(ModelView(Class, db.session))
admin.add_view(ModelView(Student, db.session))


if __name__ == "__main__":
    db.create_all()