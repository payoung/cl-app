"""
Models for CL App
"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, backref

#engine = sqlalchemy.create_engine('sqlite:///cl_app.db', echo=False)
engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    searchs = relationship("Search", backref="user", lazy='dynamic')


class Search(Base):
    __tablename__ = 'searches'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    string = Column(String)
    status = Column(Integer, default = 0)
    last_update = Column(Date)

    results = relationship("Result", backref="search")
    user_id = Column(Integer, ForeignKey('users.id'))


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    link = Column(String)

    search_id = Column(Integer, ForeignKey('searches.id'))


Base.metadata.create_all(engine)
    

