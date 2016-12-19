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
	
	def get(self):
		assert self.site, 'No site to scrape from specified'
		self.request = requests.get(site)
		self.text = self.request.text
		return self.text

	def scrape(self):
		assert self.text, 'No text retrieved yet'
		for s in self.actions:
			next_func = None
			if queue.full():
				s.execute(self, False)()
				break
			else:
				next_func = s.execute(self, True)
		return none 

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

class Write_Action(Action):
	def __init__(self, fallback_action = Action.fallback_action):
		self.fallback_action = fallback_action
	
	def act(self, scraper):
		def act():
			target_file = open(self.file_name, 'a')
			for s in scraper.write_strings:
				target_file.write(s + '\n')
			scraper.write_strings = []
		return act

