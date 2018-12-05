import time
from gi.repository import GLib
from threading import Event, Thread

class Watchdog:
	def __init__(self, timeout, handler):
		self.timeout = timeout
		self.start = None
		self.handler = handler
	
	def activity(self):
		self.start = time.time()
	
	def watch_start(self):
		def target():
			self.start = time.time()
			onTime = True
			while(onTime):
				elapset = time.time() - self.start
				if elapset > self.timeout:
					onTime = False
			GLib.idle_add(self.handler)
		thread = Thread(target=target)
		thread.daemon = True
		thread.start()


	
