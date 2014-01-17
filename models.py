from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
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
    alert_interval = Column(Integer)
    email_alert = Column(Boolean)
    text_alert = Column(Boolean)
    alert_status = Column(Boolean)
    last_update = Column(Date)

    results = relationship("Scrape", backref="alert")
    user_id = Column(Integer, ForeignKey('users.id'))


class Scrape(Base):
    __tablename__ = 'scrapes'

    id = Column(Integer, primary_key=True)
    post_ids = Column(String)
    dates = Column(String)
    descs = Column(String)
    prices = Column(String)
    links = Column(String)

    alert_id = Column(Integer, ForeignKey('alerts.id'))

    

