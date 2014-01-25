from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin
from database import Base


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)

    searches = relationship("Alert", backref="user", lazy='dynamic')


class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    interval = Column(Integer)
    email = Column(Boolean)
    text = Column(Boolean)
    status = Column(Boolean)
    last_24 = Column(Integer)
    post_cnt = Column(Integer)
    last_update = Column(DateTime)

    results = relationship("Scrape", backref="alert")
    user_id = Column(Integer, ForeignKey('users.id'))


class Scrape(Base):
    __tablename__ = 'scrapes'

    id = Column(Integer, primary_key=True)
    dt = Column(DateTime)
    post_ids = Column(String)
    dates = Column(String)
    descs = Column(String)
    prices = Column(String)
    links = Column(String)
    new_posts = Column(Integer)

    alert_id = Column(Integer, ForeignKey('alerts.id'))

