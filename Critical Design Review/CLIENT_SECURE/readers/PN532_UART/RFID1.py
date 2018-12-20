from pynfc import Nfc, Desfire, Timeout

class RFID:
	def __init__(self):
		self.reader=Nfc("pn532_uart:/dev/ttyAMA0:115200")

	def read(self):
		for target in self.reader.poll():
			try:
				id=target.uid
				return id
			except Timeout:
				pass

if __name__=="__main__":
	rfid=RFID()
	id=rfid.read()
	print("User ID: ", id.upper())
