#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://www.jb51.net/article/49789.htm

from sqlalchemy import MetaData, Sequence, Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
# from app import db


metadata = MetaData(schema="cusco")
Base = declarative_base(metadata=metadata)

# Base.metadata.create_all(db.engine)
class Role(Base):
    __tablename__ = "tb_role"
    id = Column(Integer, Sequence("seq_role_id"), primary_key=True)
    name = Column(String(64), nullable=False)
    default = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return "<Role: %s>" % self.name


# query = db.session.query(Employee)
# for e in query:
#     print(e)
class Employee(Base):
    __tablename__ = "tb_employee"
    id = Column(Integer, Sequence("seq_employee_id"), primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(32), nullable=False)
    gender = Column(String(16), nullable=False)

    def __repr__(self):
        return "<Employee %s %s>" % (self.last_name, self.first_name)


# query = db.session.query(User)
# for u in query:
#     ...
class User(Base):
    __tablename__ = "tb_user"

    id = Column(Integer, Sequence("seq_user_id"), primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(32), nullable=False)
    gender = Column(String(16), nullable=False)
    user_name = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(128))

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


class SubshopRelationship(Base):
    __tablename__ = "tb_r_subshop"

    ancestor = Column(Integer, ForeignKey("tb_subshop.id"), primary_key=True)
    descendant = Column(Integer, ForeignKey("tb_subshop.id"), primary_key=True)
    depth = Column(Integer, nullable=False)


class Subshop(Base):
    __tablename__ = "tb_subshop"

    id = Column(Integer, Sequence("seq_subshop_id"), primary_key=True)
    code = Column(String(16), nullable=False)
    name = Column(Text, nullable=False)
    dsc = Column(Text)
    current = relationship("SubshopRelationship",
                            foreign_keys=[SubshopRelationship.ancestor],
                            backref=backref("ancestor1", lazy="joined"),
                            lazy="dynamic",
                            cascade="all, delete-orphan")
    children = relationship("SubshopRelationship",
                            foreign_keys=[SubshopRelationship.descendant],
                            backref=backref("descendant1", lazy="joined"),
                            lazy="dynamic",
                            cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Subshop, self).__init__(**kwargs)
        parent = kwargs.pop("parent", None)
        chlidren = kwargs.pop("chlidren", None)
        if parent is not None:
            self.parent = parent
        for c in chlidren:
            self.children.append(c)
        # self.parent.append(Subshop(parent=self))
        # self.children.append(Subshop(children=self))

    def __repr__(self):
        return "<Subshop %r -- %r >" % (self.code, self.name)
