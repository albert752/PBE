from time import sleep
from pprint import pprint as pp
class RFID:
    def __init__(self):
        pass

    # return uid in hexa str
    def read_uid(self, vervose = False):
        sleep(3);
        return " 0x4b 0x1 0x1 0x0 0x4 0x8 0x4 0xb6 0xab 0x28 0x83"

if __name__ == "__main__":
    rf = RFID()
    uid = rf.read_uid()
    print(uid)
