import urllib2
from bs4 import BeautifulSoup
from database import db_session
from models import *
from json import dumps
from apscheduler.scheduler import Scheduler
import datetime
from sqlalchemy import desc


sched = Scheduler()


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


@sched.interval_schedule(hours=2)
def main():
    alerts = db_session.query(Alert).all()

    for alert in alerts:
        soup = url_to_soup(alert.link)
        ids, dates, descs, prices, links = pull_data(soup)
        last_update = db_session.query(Scrape).filter_by(alert=alert).order_by(desc('dt')).first()
        new_post_cnt = 0
        if last_update != None:
            for i in ids:
                if i not in last_update.post_ids:
                    new_post_cnt +=1
        scrape = Scrape(post_ids=dumps(ids), dates=dumps(dates), 
                        descs=dumps(descs), prices=dumps(prices), 
                        links=dumps(links), dt=datetime.datetime.now(),
                        new_posts=new_post_cnt, alert=alert)
        db_session.add(scrape)
        db_session.commit()
    
    print "Scheduled job was run:", datetime.datetime.now()

sched.start()

while True:
    pass
