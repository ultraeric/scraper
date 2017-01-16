import asyncio
import threading

#This is a singleton class that keeps track of the singletons of the module

class _Action_Queue(asyncio.Queue):
	"""Queue that the actions are submitted to, handles multithreading inherently. Singleton available in the variable 'action_queue'"""


	def __init__(self, max_size = 10000, num_threads = 1):
		"""Constructor.
	
		Args:
		  max_size <int>: maximum size of the queue
		  num_threads <int>: number of threads to use
		"""
		
		asyncio.Queue.__init__(self, max_size)
		self.num_threads = num_threads
		self.tracked_scrapers = []

	
	def run(self):
		"""Runs the queue, goes through all of the actions and their recursive definitions."""
	
		threads = []
		for i in range(self.num_threads):
			threads.append(_Action_Queue_Thread(name = '_Action_Queue_Thread' + str(i), action_queue = self))
		for thread in threads:
			thread.start()
		print(threading.activeCount())	
		for thread in threads:
			thread.join()	


	def populate_queue(self):
		for scraper in self.tracked_scrapers:
			scraper.populate_queue()
		 

action_queue = _Action_Queue() 


class _Action_Queue_Thread(threading.Thread):
	"""A worker thread that handles actions. Should be hidden from the API."""
		

	def __init__(self, name = '_Action_Queue_Thread', description = 'Queue worker thread',  action_queue = action_queue):
		"""Constructor.

		Args:
		  name <string>: a name for this thread
		  description <string>: a description for this thread
		  action_queue <_Action_Queue>: the action queue that this thread draws Actions from.
		"""

		threading.Thread.__init__(self)
		self.name = name
		self.description = description
		self.action_queue = action_queue
	
	def run(self):
		while not self.action_queue.empty():
			action = self.action_queue.get_nowait()
			action()

