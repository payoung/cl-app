import urllib2
#from bs4 import BeautifulSoup

def to_text(address, text_file):
	
	html = urllib2.urlopen(address).read() 


	#soup = BeautifulSoup(html)

	#s_doc = soup.prettify()

	target = open(text_file, 'w')
	target.truncate()
	target.write(html)
	target.close()

address = 'http://sfbay.craigslist.org/search/jjj?catAbb=jjj&query=python&zoomToPosting=&addFour=part-time'
txt = 'CL-PartTime-Python-Search.txt'

to_text(address, txt)

"""
address = []
address.append('http://www.swellinfo.com/surf-forecast/ocean-beach-california-nw')
address.append('http://www.swellinfo.com/surf-forecast/ocean-beach-california')
address.append('http://www.swellinfo.com/surf-forecast/half-moon-bay-california')
address.append('http://www.swellinfo.com/surf-forecast/pescadero-california')
address.append('http://www.swellinfo.com/surf-forecast/davenport-california')
address.append('http://www.swellinfo.com/surf-forecast/santa-cruz-california')

txt = []
txt.append('Ocean Beach North.txt')
txt.append('Ocean Beach South.txt')
txt.append('Half Moon Bay.txt')
txt.append('Pescadero.txt')
txt.append('Davenport.txt')
txt.append('Santa Cruz.txt')

for i in range(len(address)):
	to_text(address[i], txt[i])
"""

