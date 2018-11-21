import threading
import time
from RFID1 import RFID
from gi.repository import GLib

class ReaderThread:
	def __init__(self, isTest=False, handler):
		self.reader=RFID()
		self.handler=handler
	def startReader(self):
		self.thread=threading.Thread(target=self.readUID, args=[self.handler])
		self.thread.daemon=True
		self.thread.start()

	def readUID(self, handler):
		GLib.idle_add(handler, self.reader.read())

