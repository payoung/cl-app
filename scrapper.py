import urllib2
from bs4 import BeautifulSoup
from database import db_session
from models import *
from json import dumps
from apscheduler.scheduler import Scheduler
import datetime


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
        scrape = Scrape(post_ids=dumps(ids), dates=dumps(dates), 
                        descs=dumps(descs), prices=dumps(prices), 
                        links=dumps(links), alert=alert)
        db_session.add(scrape)
        db_session.commit()
    
    print "Scheduled process was run:", datetime.datetime.now()

sched.start()

while True:
    pass


#address = 'http://sfbay.craigslist.org/search/ggg?zoomToPosting=&catAbb=ggg&query=python&addThree=&excats='
#address = 'http://sfbay.craigslist.org/search/sga?catAbb=sga&query=surfboard+hybrid&zoomToPosting=&minAsk=&maxAsk='

#soup = url_to_soup(address)
#post_ids, post_dates, post_descs, post_prices, post_links = pull_data(soup)

