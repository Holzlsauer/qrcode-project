from app import db
from sqlalchemy.dialects.postgresql import JSON

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from config import Config

# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
# Base = declarative_base()


class User(db.Model):
    __tablename__ = "users"

    id = Column(db.Integer, primary_key=True)
    username = Column(db.String())
    password = Column(db.String())
    user_type = Column(db.Integer)  # Professor or student (1 or 2)
    timestamp = Column(db.Float)
    user_token = Column(db.String())

    def __init__(self, username, password, user_type, timestamp, user_token):
        """docstring 2"""
        self.username = username
        self.password = password
        self.user_type = user_type
        self.timestamp = timestamp
        self.user_token = user_token

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ProfessorClass(db.Model):
    """docstrin 1"""
    __tablename__ = "professor_class"

    id = Column(db.Integer, primary_key=True)
    professor_id = Column(db.Integer, ForeignKey("users.id"))
    class_code = Column(db.Integer, ForeignKey("classes.id"))
    professor = relationship("User", backref="professor_classs")
    code = relationship("Classes", backref="professor_classs")

    def __init__(self, professor_id, class_code):
        """docstring 2"""
        self.professor_id = professor_id
        self.class_code = class_code

    def __repr__(self):
        return '<id {}>'.format(self.id)


class StudentClass(db.Model):
    """docstrin 1"""
    __tablename__ = "student_class"

    id = Column(db.Integer, primary_key=True)
    student_id = Column(db.Integer, ForeignKey("users.id"))
    class_code = Column(db.Integer, ForeignKey("classes.id"))
    student = relationship("User", backref="student_classs")
    code = relationship("Classes", backref="student_classs")

    def __init__(self, student_id, class_code):
        """docstring 2"""
        self.student_id = student_id
        self.class_code = class_code

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Classes(db.Model):
    """docstrin 1"""
    __tablename__ = "classes"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String())
    code = Column(db.String())
    date = Column(db.String())
    time_start = Column(db.String())
    time_end = Column(db.String())

    def __init__(self, name, code, date, time_start, time_end):
        """docstring 2"""
        self.name = name
        self.code = code
        self.date = date
        self.time_start = time_start
        self.time_end = time_end

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Presences(db.Model):
    """docstring 1"""
    __tablename__ = "presences"

    id = Column(db.Integer, primary_key=True)
    user_id = Column(db.Integer,  ForeignKey("users.id"))
    class_code = Column(db.String())
    token = Column(db.String())
    token_expire = Column(db.Float)  # date + duração
    presence = Column(db.Boolean)
    num_classes = Column(db.Integer)
    date = Column(db.Float)  # Timestamp
    confirmation_date = Column(db.Float)
    user = relationship("User", backref="presencess")

    def __init__(self, user_id, class_code, token, token_expire, presence, num_classes, date, confirmation_date):
        """docstring 2"""
        self.user_id = user_id
        self.class_code = class_code
        self.token = token
        self.token_expire = token_expire
        self.presence = presence
        self.num_classes = num_classes
        self.date = date
        self.confirmation_date = confirmation_date

    def __repr__(self):
        return '<id {}>'.format(self.id)


# create tables
# Base.metadata.create_all(engine)
