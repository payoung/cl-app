from database import db_session
from models import *
import datetime

def add_test_data():
    user = User(name="Paul", email="fake@email.com", password="password", phone="+14155779330")
    db_session.add(user)
    db_session.commit()
    link1 = 'http://sfbay.craigslist.org/search/ggg?zoomToPosting=&catAbb=ggg&query=python&addThree=&excats='
    link2 = 'http://sfbay.craigslist.org/search/sga?catAbb=sga&query=surfboard+hybrid&zoomToPosting=&minAsk=&maxAsk='
    link3 = 'http://sfbay.craigslist.org/search/mca?zoomToPosting=&catAbb=mca&query=&minAsk=0&maxAsk=1000&excats='

    alert1 = Alert(name="Python Gigs", link=link1, interval=12, 
                    email=True, text=True, status=True, last_24=0, post_cnt=0, 
                    last_update=datetime.datetime.now(), user=user)
    db_session.add(alert1)
    db_session.commit()
    alert2 = Alert(name="Surfboard - hybrid", link=link2, interval=12,
                    email=True, text=True, status=True, last_24=0, post_cnt=0,
                    last_update=datetime.datetime.now(), user=user)
    db_session.add(alert2)
    db_session.commit()
    alert3 = Alert(name='Cheap Motorcycles', link=link3, interval=1,
                    email=True, text=True, status=True, last_24=0, post_cnt=0,
                    last_update=datetime.datetime.now(), user=user)
    db_session.add(alert3)
    db_session.commit()
    print "Test data added to db."

