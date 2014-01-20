from database import db_session
from models import *
import datetime

def add_test_data():
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
    alert2 = Alert(name="Surfboard - hybrid", link=link2, alert_interval=12,
                    email_alert=True, text_alert=True, alert_status=True,
                    last_update=datetime.date.today(), user=user)
    db_session.add(alert1)
    db_session.commit()
    print "Test data added to db."
