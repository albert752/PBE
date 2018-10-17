from py532lib.i2c import Pn532_i2c as pn532
import threading
from time import sleep

class RFID:
    def __init__(self, test = False):
        if not test:
            self.reader = pn532()
            self.reader.SAMconfigure()
        self.test = test



    def _read(self, vervose = False):
        card_data = self.reader.read_mifare().get_data()
        output = ""
        for byte in card_data:
            if vervose:
                print(hex(byte), end =" ")
            output = " ".join([output, hex(byte)])
        self.reader.reset_i2c()
        return output

    def readThread(self, handler):
        self.thread = threading.Thread(target=self.readUID(handler))
        self.thread.daemon = True
        self.thread.start()

    def readUID(self, handler):
        if not self.test:
            values = self._read()
            uid = values.split(" ")[8:].replace("0x", "")
            return uid.upper()
        else:
            sleep(3)
            handler("3B8C9A2H")
            return "3B8C9A2H"



if __name__ == "__main__":
    rf = RFID()
    uid = rf._readUID()
    print(uid)
