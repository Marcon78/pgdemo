#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://www.jb51.net/article/49789.htm

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


metadata = MetaData(schema="cusco")
Base = declarative_base(metadata=metadata)


class Role(Base):
    __tablename__ = "tb_role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    default = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return "<Role: %s>" % self.name


# query = db.session.query(Employee)
# for e in query:
#     print(e)
class Employee(Base):
    __tablename__ = "tb_employee"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return "<Employee %s %s>" % (self.last_name, self.first_name)


# query = db.session.query(User)
# for u in query:
#     ...
class User(Base):
    __tablename__ = "tb_user"

    id = db.Column(db.Integer, primary_key=True)            # from Employee
    first_name = db.Column(db.String(64), nullable=False)   # from Employee
    last_name = db.Column(db.String(32), nullable=False)    # from Employee
    gender = db.Column(db.String(16), nullable=False)       # from Employee
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User %s %s(%s)>" % (self.last_name, self.first_name, self.user_name)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
