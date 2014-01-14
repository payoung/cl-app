import urllib2
from bs4 import BeautifulSoup

def url_to_soup(address):
    html = urllib2.urlopen(address).read()
    soup = BeautifulSoup(html)
    return soup

def pull_data(soup):
    post_ids = []
    post_dates = []
    post_descs = []
    post_price = []
    post_links = []

    for p in soup.findAll("p"):
        post_ids.append(p.get('data-pid'))
        post_dates.append(p.contents[5].span.get_text())
        post_descs.append(p.contents[5].a.get_text())
        price = p.contents[1].find(class_="price")
        if price != None:
            post_price.append(price.get_text())
        else:
            post_price.append(price)
        post_links.append(p.contents[1].get('href'))

    return post_ids, post_dates, post_descs, post_price, post_links

address = 'http://sfbay.craigslist.org/search/sga?catAbb=sga&query=surfboard+hybrid&zoomToPosting=&minAsk=&maxAsk='

soup = url_to_soup(address)
post_ids, post_dates, post_descs, post_price, post_links = pull_data(soup)

