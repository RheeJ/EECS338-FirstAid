import urllib2
from bs4 import BeautifulSoup

class Collection(object):
	def __init__(self):
		self.scrapers = []
		self.manuals = []

	def append_scraper(self, scraper):
		self.scrapers.append(scraper)

	def detect_collision(self):
		for scraper in self.scrapers:
			for instructions in scraper.instructions:
				if instruction.name not in self.unique:
					self.manuals.append(instruction)

class Scraper(object):
	def __init__(self, tag, source):
		self.tag = tag
		self.source = source
		self.urls = []
		self.instructions = []

class MayoScraper(Scraper):
	def __init__(self, tag):
		Scraper.__init__(self, tag, "Mayo")

	def fetch_urls(self):
		#Make request
		url = "http://www.mayoclinic.org/first-aid"
		req = urllib2.Request(url)
		site = urllib2.urlopen(req)
		html = site.read()
		
		#Start parsing urls
		soup = BeautifulSoup(html, 'html.parser')
		main = soup.find('div', attrs={'id' : 'main-content'})
		for a in main.find_all('a', href=True):
			self.urls.append(url + a['href'])

	def parse_instructions(self, url):
		req = urllib2.Request(url)
		site = urllib2.urlopen(req)
		html = site.read()

		soup = BeautifulSoup(html, 'html.parser')
		main = soup.find('div', attrs={'id' : 'main-content'})
		main_html = main.prettify("utf-8")
		main_split = main_html.split('<!--googleoff: snippet-->')
		partitions = main_split[0].split('<h3>')
		for i in range(0, len(partitions)):
			if i != 0:
				partitions[i] = '<h3>' + partitions[i] 
			print partitions[i]
			print ""
			print ""



class Instructions(object):
	def __init__(self, name, keywords, steps):
		self.name = name
		self.keywords = keywords
		self.steps = steps



