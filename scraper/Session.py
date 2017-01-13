import queue

class _queue(queue.Queue):
	def __init__(self, max_size = 10000):
		super().__init__(max_size)
	
	def run(self):
		while not self.empty():
			action = self.get()
			action()

action_queue = _queue() 
queue = None
