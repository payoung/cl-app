from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URI = 'sqlite:///tmp/cl_app.db'

engine = create_engine(DATABASE_URI, echo=False)
#engine = create_engine('sqlite:///:memory:', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import *
    Base.metadata.create_all(bind=engine)  
