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

    def start(self, handler):
        self.thread = threading.Thread(target=self.readUID, args=[handler])
        self.thread.daemon = True
        self.thread.start()

    def _parseUID(self):
        if not self.test:
            values = self._read()

        else:
            sleep(3)
            values = "0x3b 0x5c 0x3a 0x7b 0x2d 0x9a 0x8c 0x6e 0x3b 0x8c 0x9a 0x2c"
        uid = values.split(" ")[8:]
        uid = "".join(uid).replace("0x", "")
        return uid.upper()


    def readUID(self, handler):
        while True:
            handler(self._parseUID())


if __name__ == "__main__":
    rf = RFID()
    uid = rf._readUID()
    print(uid)
