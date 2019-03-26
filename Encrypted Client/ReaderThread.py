from RFID import RFID
import threading
from gi.repository import GLib

class ReaderThread:
	def __init__(self, isTest, handler):
		self.reader = RFID(isTest)
		self.handler = handler

	def startReader(self, join = False):
		""" Creates and starts the reader thread.
		:param handler: GUI handler to manage the read info.
		:param join: If it is been executed from the main of this module,
		waits for the thread to end (never ends) to end teh exection of the
		program. I prevents the program quit and kill the thread.
		:return: None
		"""
		thread = threading.Thread(target=self.readUID, args=[])
		thread.daemon = True
		thread.start()

	def readUID(self):
		""" Main infinite loop. Executes the GUI handler function each time a card is read.
		:param handler: GUI handler to manage the read info.
		:return: None
		"""
		GLib.idle_add(self.handler, self.reader.readUID())
