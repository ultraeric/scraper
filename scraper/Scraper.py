import request
import re
import xml.etree.ElementTree
from asyncio import Queue

r = requests.get('https://www.google.com/finance')
regex = r'(?:rel=nofollow\s*id=n-hp-\s*>)(.*)<\/a'
s = re.findall(regex, r.text)
for i in s:
	print(i)

#Worker class that scrapes information from a site given a few actions. Running the actions returns a higher-order function that must be submitted to a queue. 
class Scraper():
	def __init__(self, site = None, actions = None, queue = None):
		"""Constructor.
		
		Args:
		  site: initial uri of the site to be visiting. string
		  actions: a list of actions to be run. 
		  queue: the queue that the jobs will be submitted to
		"""
		self.site = site
		self.actions = actions

		#Text results of a regex-based search through the text of the HTML document
		self.found_strings = []

		#Request object from requests library representing result of an HTTP request	
		self.request = None

		#Text from an HTTP request (HTML document)
		self.text = ''	

		#Recursive links to follow
		self.links = []

		#The XML tree of the HTML document
		self.xml_tree = None		

		#The job queue that this scraper will submit to
		self.queue = queue
	
		#The XML elements of the HTML document that are of interest
		self.xml_elements = []

	def populate_queue(self):
		to_act = True
		for s in self.actions:
			next_func = None
			if queue.full():
				to_act = False
				s.run(self, to_act)()
			else:
				next_func = s.run(self, to_act)
				queue.put(next_func)
		return None 

#Interface that all Actions should follow. Call Action.run() from outside, override Action.act() when conforming to the interface.
#Actions act on the data source, Scraper. Actions can create new actions that should take no parameters and submit them to the queue
class Action():
	def __init__(self, fallback_action = None):
		if fallback_action:
			self.fallback_action = fallback_action
	#Immediately execute action
	def execute(self, scraper = None, act = True):
		return self.run(scraper)()

	#User should not override as part of interface
	def run(self, scraper = None, act = True):
		if not act or not scraper or scraper.queue.full():
			return self.fallback_action.run(scraper)()
		scraper.queue.put(self.get_act(scraper))

	def get_act(self, scraper):
		return

#DO NOT OVERRIDE 
#The default fallback action for failed actions
class Default_Fallback_Action(Action):
	def __init__(self, fallback_action = None):
		return
		
	def run(self, scraper = None, act = None):
		return lambda: None
	
	def get_act(self, scraper):
		return lambda: None

Action.fallback_action = Default_Fallback_Action()

#HTTP GET request
#TODO: implement authentication
class Get_Action(Action):
	def get_act(self, scraper):
		def act():
			if not scraper.site:
				return
			scraper.request = requests.get(scraper.site)
			scraper.text = scraper.request.text
		return act

#Writes all the strings currently in the Scraper's found_strings found through Find_Strings_Action
class Write_Action(Action):
	def __init__(self, file_name, regexes = None, fallback_action = None):
		super().__init__(fallback_action)
		self.file_name = file_name
		
	def get_act(self, scraper):
		def act():
			target_file = open(self.file_name, 'a')
			for s in scraper.found_strings:
				target_file.write(s + '\n')
			scraper.found_strings = []
		return act

class Find_Strings_Action(Action):
	def __init__(self, regexes, fallback_action = None):
		super().__init__(fallback_action)
		if not isinstance(regexes, list):
			self.regexes = [regexes]
		else:
			self.regexes = regexes

	def get_act(self, scraper):
		def act():
			for reg in self.regexes:
				matches = re.findall(reg, scraper.text)
				scraper.found_strings.extend(matches)
		return act

class Find_Links_Action(Find_Strings_Action):
	def get_act(self, scraper):
		def act():
			for reg in self.regexes:
				matches = re.findall(reg, scraper.text)
				scraper.links.extend(matches)
			print(type(scores))
				scraper.found_strings.extend(matches)
		return act

class Scrape_Next_Link_Action(Action):
	def get_act(self, scraper):
		def act():
			scraper.site = scraper.links.pop(0)
			scraper.scrape()
		return act

class Parse_XML_Action(Action):
	def get_act(self, scraper):
		def act():
			if not scraper.text:
				Get_Action().execute(scraper)
			scraper.xml_tree = xml.etree.ElementTree.parse(scraper.text)
		return act

class Find_XML_Elements_Action(Action):
	def __init__(self, tag = '', attributes = {}, fallback_action = None)
		super().__init__(self, fallback_action)
		self.tag = tag
		self.attributes = attributes

	def get_act(self, scraper):
		def act():
			if not scraper.xml_tree:
				Parse_XML_Action().execute(scraper)
			def find(element):
				if element.tag == self.tag or not self.tag:
					if all([(key is in element.attrib and element.attrib[key] == self.attributes[key]) for key in self.attributes]):
						scraper.xml_elements.append(element)
				for sub_element in element:
					find(sub_element)	
			find(scraper.xml_tree)
		return act
