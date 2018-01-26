#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


class User(db.Model):
    __tablename__ = "tb_user"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
