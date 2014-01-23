import urllib2
from bs4 import BeautifulSoup
from database import db_session
from models import *
from json import dumps
from apscheduler.scheduler import Scheduler
import time
import datetime
from sqlalchemy import desc
from twilio.rest import TwilioRestClient
from credentials import twilio_account_sid, twilio_auth_token, twilio_phone

sched = Scheduler()

'''
Scrapping Tasks
'''

def url_to_soup(address):
    html = urllib2.urlopen(address).read()
    soup = BeautifulSoup(html)
    return soup


def pull_data(soup):
    ids = []
    dates = []
    descs = []
    prices = []
    links = []

    for p in soup.findAll("p"):
        ids.append(p.get('data-pid'))
        dates.append(p.contents[5].span.get_text())
        descs.append(p.contents[5].a.get_text())
        price = p.contents[1].find(class_="price")
        if price != None:
            prices.append(price.get_text())
        else:
            prices.append(price)
        links.append(p.contents[1].get('href'))

    return ids, dates, descs, prices, links


def scrape(alerts):

    for alert in alerts:
        soup = url_to_soup(alert.link)
        ids, dates, descs, prices, links = pull_data(soup)
        last_update = db_session.query(Scrape).filter_by(alert=alert).order_by(desc('dt')).first()
        new_post_cnt = 0
        if last_update != None:
            for i in ids:
                if i not in last_update.post_ids:
                    new_post_cnt +=1
        now = datetime.datetime.now()
        scrape = Scrape(post_ids=dumps(ids), dates=dumps(dates), 
                        descs=dumps(descs), prices=dumps(prices), 
                        links=dumps(links), dt=now,
                        new_posts=new_post_cnt, alert=alert)
        db_session.add(scrape)
        db_session.commit()
        #update the last_24 field in the alerts table by getting the last 12 scrapes (assuming
        #that the scrapes are done every 2 hours) and adding up any new posts
        past_12 = db_session.query(Scrape).filter_by(alert=alert).order_by(desc('dt')).limit(12)
        delta24 = datetime.timedelta(hours=24)
        last_24 = 0
        for past in past_12:
            if now - past.dt <= delta24:
                last_24 += past.new_posts
        alert.last_24 = last_24
        db_session.add(alert)
        db_session.commit()
    print "Scheduled scrape was run:", datetime.datetime.now()

'''
Messaging Tasks
'''

# function for sending text messages through the Twilio API
def send_text(alerts):

    # Your Account Sid and Auth Token from twilio.com/user/account
    client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    now = datetime.datetime.now()

    for alert in alerts:
        if alert.status and alert.text:
            alert_delta = datetime.timedelta(hours=alert.interval)
            if now - alert.last_update >= alert_delta:
                user = alert.user
                body = "CL Alerts: " + alert.name + " - There have been " + str(alert.last_24) + " new posts in the last 24 hours."
                message = client.sms.messages.create(body=body,
                    to=user.phone,
                    from_=twilio_phone)
                print "Message sent to:", user.name, datetime.datetime.now()


'''
Start Scheduler and run infinite loop
'''

@sched.interval_schedule(hours=1)
#@sched.cron_schedule(hour='0,2,4,6,8,10,12,14,16,18,20,22')
def run_tasks():
    alerts = db_session.query(Alert).all()
    scrape(alerts)
    send_text(alerts)
    print "Scheduled tasks were run ", datetime.datetime.now()
    #send_email(alerts)


sched.start()

while True:
    time.sleep(1)
    pass
