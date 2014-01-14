from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin
from database import Base


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    searches = relationship("Search", backref="user", lazy='dynamic')


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

    

