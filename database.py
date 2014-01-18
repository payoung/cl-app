from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine(DATABASE_URI, echo=False)
#engine = create_engine('sqlite:///:memory:', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	from models import *
	Base.metadata.create_all(bind=engine)

def add_test_data():
    from models import *
    import datetime
    user = User(name="Paul", email="fake@email.com", password="password", phone="123-123-1234")
    db_session.add(user)
    db_session.commit()
    link1 = 'http://sfbay.craigslist.org/search/ggg?zoomToPosting=&catAbb=ggg&query=python&addThree=&excats='
    link2 = 'http://sfbay.craigslist.org/search/sga?catAbb=sga&query=surfboard+hybrid&zoomToPosting=&minAsk=&maxAsk='
    alert1 = Alert(name="Python Gigs", link=link1, alert_interval=12, 
                    email_alert=True, text_alert=True, alert_status=True,
                    last_update=datetime.date.today(), user=user)
    db_session.add(alert1)
    db_session.commit()
    alert2 = Alert(name="Surfboard - hybrid", link=lin2, alert_interval=12,
                    email_alert=True, text_alert=True, alert_status=True,
                    last_update=datetime.date.today(), user=user)
    db_session.add(alert1)
    db_Session.commit()
    print "Test data added to db."
  
