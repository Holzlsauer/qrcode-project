from database import db

from sqlalchemy import Column, Date, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String())
    password = Column(String())
    user_type = Column(Integer)  # Professor or student (1 or 2)
    timestamp = Column(Float)
    user_token = Column(String())

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

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey("users.id"))
    class_code = Column(Integer, ForeignKey("classes.id"))
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

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    class_code = Column(Integer, ForeignKey("classes.id"))
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

    id = Column(Integer, primary_key=True)
    name = Column(String())
    code = Column(String())
    date = Column(String())
    time_start = Column(String())
    time_end = Column(String())

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

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,  ForeignKey("users.id"))
    class_code = Column(String())
    token = Column(String())
    token_expire = Column(Float)  # date + duração
    presence = Column(Boolean)
    num_classes = Column(Integer)
    date = Column(Float)  # Timestamp
    confirmation_date = Column(Float)
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
