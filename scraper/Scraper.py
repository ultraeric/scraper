import requests
import re
import xml.etree.ElementTree

r = requests.get('https://www.google.com/finance')
regex = r'(?:rel=nofollow\s*id=n-hp-\s*>)(.*)<\/a'
s = re.findall(regex, r.text)
for i in s:
	print(i)

class Scraper():
	"""Worker class that scrapes information from a site given a few Actions. 
	Running the Actions returns a higher-order function that is submitted to 
	the package-wide queue. Note that this class, Scraper acts as a data source
	for Actions, and Actions act on the Scraper. Scraper should contain all the
	data that an Action uses and should have no functionality on its own.
	"""

	queue = None

	def __init__(self, site = None, actions = [], queue = None):
		"""Constructor.
		
		Args:
		  site <string>: initial uri of the site to be visiting. 
		  actions <list of Actions>: a list of actions to be run.  
		  queue <Session.queue>: the queue that the jobs will be submitted to, 
			   		   which lives in the package singleton.
		"""

		#Site to scrape on
		self.site = site
		#Initial actions
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

		if queue:	
			#The job queue that this scraper will submit to
			self.queue = queue
		#The XML elements of the HTML document that are of interest
		self.xml_elements = []


	def populate_queue(self):
		"""Initialize the Scraper and its Actions.
		"""

		to_act = True
		for s in self.actions:
			#Runs fallback_action if queue is full.
			if self.queue.full():
				to_act = False
				s.run(self, to_act)()
			else:
				next_func = s.run(self, to_act)
				self.queue.put(next_func)
		return 



class Action():
	"""Interface that all Actions should extend. You should call Action.run()
	to run the Action, and it will be run when the next available 
	resource is up. To run it immediately, use Action.execute() to 
	immediately run the Action. To extend the Action, override get_act().
	"""
	

	def __init__(self, fallback_action = None):
		"""Constructor.
		
		Args:
		  fallback_action <Action>: action to run when package singleton determines Action
				     has failed 
		"""

		if fallback_action:
			self.fallback_action = fallback_action


	def execute(self, scraper = None, act = True):
		"""Executes the Action immediately. DO NOT OVERRIDE.

		Args:
		  scraper <Scraper>: the Scraper that this Action acts on
		  act <boolean>: passed in as False if package singleton determines Action has failed

		Returns:
		  @get_act(scraper)
		"""

		return self.get_act(scraper)()


	def run(self, scraper = None, act = True):
		"""Adds Action to queue and runs it when the resources are available. DO NOT OVERRIDE.

		Args:
		  scraper <Scraper>: the Scraper that this Action acts on
		  act <boolean>: passed in as False if package singleton determines Action has failed
		"""

		if not act or not scraper or scraper.queue.full():
			return self.fallback_action.run(scraper)()
		scraper.queue.put(self.get_act(scraper))


	def get_act(self, scraper):
		"""Creates action. Higher-order function.
	
		Args:
		  scraper <Scraper>: the Scraper that this Action acts on
	
		Returns: 
		  function to submit to queue
		"""

		return



class Default_Fallback_Action(Action):
	"""DO NOT OVERRIDE"""

	
	def __init__(self, fallback_action = None):
		return
			
	def run(self, scraper = None, act = None):
		return lambda: None
	
	def get_act(self, scraper):
		return lambda: None



Action.fallback_action = Default_Fallback_Action()



class Recursive_Action(Action):
	"""Defines a recursive scraping behavior"""
	

	def __init__(self, recursing_actions = [], fallback_action = None):
		"""Constructor.

		recursing_actions <list of Actions>: a list of Actions that will be 
			re-inserted into the Action queue once this is run. Helps
			define the followup of recursive scraping.
		"""

		super().__init__(fallback_action)
		self.recursing_actions = recursing_actions

	
	def get_act(self, scraper):
		"""Creates Recursive_Action. Higher-order function.
	
		Args: @Action
		"""

		def act():		
			for action in recursing_actions:
				scraper.queue.put(action)
		return act()



class Get_Action(Action):
	"""HTTP GET request from Scraper.site."""


	def get_act(self, scraper):
		"""Creates HTTP GET request. Higher order function.

		Args: @Action
		"""

		def act():
			if not scraper.site:
				return
			scraper.request = requests.get(scraper.site)
			scraper.text = scraper.request.text
		return act



class Write_Action(Action):
	"""Writes found_strings to a file."""


	def __init__(self, file_name, fallback_action = None):
		"""Constructor.

		Args: 
		  file_name <string>: name of file to write to
		  fallback_action <Action>: @Action
		"""
	
		super().__init__(fallback_action)
		self.file_name = file_name
	
	
	def get_act(self, scraper):
		"""Creates Write_Action. Higher-order function.
	
		Args: @Action
		"""
		def act():
			target_file = open(self.file_name, 'a')
			for s in scraper.found_strings:
				target_file.write(s + '\n')
			scraper.found_strings = []
		return act



class Find_Strings_Action(Action):
	"""Find Strings given a set of regular expressions to match to."""


	def __init__(self, regexes, fallback_action = None):
		"""Constructor.
	
		Args:
		  regexes <list of regexes>: regular expressions to match
		  fallback_action <Action>: @Action
		"""

		super().__init__(fallback_action)
		if not isinstance(regexes, list):
			self.regexes = [regexes]
		else:
			self.regexes = regexes


	def get_act(self, scraper):
		"""Creates Find_Strings_Action. Higher order function.

		Args: @Action
		"""

		def act():
			for reg in self.regexes:
				matches = re.findall(reg, scraper.text)
				scraper.found_strings.extend(matches)
		return act



class Find_Links_Action(Find_Strings_Action):
	"""Finds links given a set of regular expressions.

	Constructor: @Find_Strings_Action
	"""	


	def get_act(self, scraper):
		"""Creates Find_Links_Action. Higher order function.

		Args: @Action
		"""

		def act():
			for reg in self.regexes:
				matches = re.findall(reg, scraper.text)
				scraper.links.extend(matches)
			print(type(scores))
			scraper.found_strings.extend(matches)
		return act



class Parse_XML_Action(Action):
	"""Parses the HTML document into an XML tree."""


	def get_act(self, scraper):
		"""Creates Parse_XML_Action. Higher order function.
	
		Args: @Action
		"""
	
		def act():
			if not scraper.text:
				Get_Action().execute(scraper)
			if not scraper.text:
				return
			scraper.xml_tree = xml.etree.ElementTree.parse(scraper.text)
		return act



class Find_XML_Elements_Action(Action):
	"""Find the XML elements from the XML tree in the scraper."""


	def __init__(self, tag_attribute_list = [], find_subelements = False, fallback_action = None):
		"""Constructor.

		Args:
		  tag_attribute_list <list of <pairs of <string, dictionary of <attribute, value>>>>: 
			a list of HTML tags that satisfy one or more of the tag, attribute pairs
		  find_subelements <boolean>: determines whether or not to find subelements of found XML elements
		  fallback_action <Action>: @Action
		"""	

		super().__init__(self, fallback_action)
		self.tags = [tag_attribute[0] for tag_attribute in tag_attribute_list]
		self.attributes = [tag_attribute[1] for tag_attribute in tag_attribute_list]
		self.find_subelements = find_subelements


	def get_act(self, scraper):
		"""Creates Find_XML_Elements_Action. Higher-order function

		Args: @Action
		"""

		def act():
			if not scraper.xml_tree:
				Parse_XML_Action().execute(scraper)
			if not scraper.xml_tree:
				return
			xml_elements = scraper.xml_elements[:]
			
			def find(element):
				"""Helper function. Recursively traverses tree to find if the elements
				satisfy the tag/attribute pairs.

				Args:
				  element <ElementTree>: the HTML element that is about to be examined
				"""

				if element.tag in self.tags or not self.tags:
					element_index = self.tags.index(element.tag)
					if all([(key in element.attrib and element.attrib[key] == self.attributes[element_index][key]) 
						for key in self.attributes[element_index]]):
						scraper.xml_elements.append(element)
				for sub_element in element:
					find(sub_element)	
			if self.find_subelements:
				for e in xml_elements:
					find(e)
			else:
				find(scraper.xml_tree)
		return act

