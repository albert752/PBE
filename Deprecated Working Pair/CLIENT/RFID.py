""" General Purpose RFID class
mode.

Example:
    With an RFID reader:
        First of all, connect the RFID reader on the apropiate pins. Here there
        is a small table:

        | pn532 | RPi B3          |
        |-------|-----------------|
        |    5V | 5V (pin 4 or 2) |
        |   GND | GND (pin 6)     |
        |   SDA | SDA0 (pin3)     |
        |   SCL | SCL0 (pin5)     |

        Then run:

        $ python3 RFID.py


    Without an RFID reader
        If your purpose is just to test the app without a reader, you can do so
        by running this command:

        $ python3 RFID.py test

        It will automatically yields the same UID every 3s.
"""

import sys
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

from time import sleep

class RFID:
    '''
    A RFID reader object. It can be run in the main thread or in a parallel thread
    :public __init__
            readUID
            start
    '''
    def __init__(self, test=False):
        """ Initializes the Reader or only the test
        :param test: If true, enter test mode
        """
        if not test:
            self.reader = Pn532_i2c()
            self.reader.SAMconfigure()
        self.test = test
        self.i = 0
    def _read(self, verbose = False):
        """ Connects and reads the card data. It is blocking.

        :param verbose: If True, prints each byte.
        :return: None
        """
        card_data = self.reader.read_mifare().get_data()
        output = ""
        for byte in card_data:
            if verbose:
                print(hex(byte), end =" ")
            output = " ".join([output, hex(byte)])

        self.reader.reset_i2c()
        return output

    def readUID(self):
        """ Extracts the User Identifier (UID) info from all the infomation read of the Mifare card

        :return: User Identifier (UID)
        """
        if not self.test:
            values = self._read()

        else:
            sleep(3)
            values = ["0x3b 0x5c 0x3a 0x7b 0x2d 0x9a 0x8c 0x6e 0x3b 0x8c 0x9a 0x29" ,"0x3b 0x5c 0x3a 0x7b 0x2d 0x9a 0x8c 0x6e 0x3b 0x8c 0x9a 0x89"]
        uid = values.split(" ")[8:]
        uid = "".join(uid).replace("0x", "")
        self.i += 1
        return uid.upper()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        isTest = sys.argv[1]=="test"
    else:
        isTest = False

    lector = RFID(isTest)
    while True:
        print("Your UID is " + lector.readUID())
