from py532lib.i2c import Pn532_i2c as pn532
from pprint import pprint as pp
class RFID:
    def __init__(self):
        self.reader = pn532()
        self.reader.SAMconfigure()

    # return uid in hexa str
    def read_uid(self, vervose = False):
        card_data = self.reader.read_mifare().get_data()
        output = ""
        for byte in card_data:
            if vervose:
                print(hex(byte), end =" ")
            output = " ".join([output, hex(byte)])
        self.reader.reset_i2c()
        return output

if __name__ == "__main__":
    rf = RFID()
    uid = rf.read_uid()
    print(uid)
