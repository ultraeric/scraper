import requests
import re
from asyncio import Queue

r = requests.get('https://www.google.com/finance')
regex = r'(?:rel=nofollow\s*id=n-hp-\s*>)(.*)<\/a'
s = re.findall(regex, r.text)
for i in s:
	print(i)

#Worker class that scrapes information from a site given a few actions. Running the actions returns a higher-order function that must be submitted to a queue. 
class Scraper():
	def __init__(self, site = None, actions = None, queue = None):
		self.site = site
		self.actions = actions
		self.write_strings = []
		self.request = None
		self.text = ''	

	def scrape(self):
		assert self.text, 'No text retrieved yet'
		for s in self.actions:
			next_func = None
			to_act = True
			if queue.full():
				to_act = False
				s.execute(self, to_act)()
			else:
				next_func = s.execute(self, to_act)
		return None 

class Action():
	def __init__(self, fallback_action):
		self.fallback_action = fallback_action

	#User should not override as part of interface
	def execute(self, scraper = None, act = True):
		if not act or not scraper:
			return self.fallback_action.execute(scraper)
		return self.act(scraper)

	def act(self, scraper):


class Fallback_Action(Action):
	def __init__(self, fallback_action = None):
		
	def execute(self, scraper = None, act = None):
		return lambda: None
	
	def act(self, scraper):
		return lambda: None

Action.fallback_action = Fallback_Action()

class Get_Action(Action):
	assert scraper.site, 'No site to scrape from specified'
	def act(self, scraper):
		def act():
			scraper.request = requests.get(scraper.site)
                	scraper.text = scraper.request.text
		return act

class Write_Action(Action):	
	def act(self, scraper):
		def act():
			target_file = open(self.file_name, 'a')
			for s in scraper.write_strings:
				target_file.write(s + '\n')
			scraper.write_strings = []
		return act

