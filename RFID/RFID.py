""" General Purpose RFID class

This module contains the implementation of RFID reader w/ the py532lib in I2C
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
from py532lib.i2c import Pn532_i2c as pn532
import threading
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
            self.reader = pn532()
            self.reader.SAMconfigure()
        self.test = test

    def _read(self, verbose = False):
        """ Connects and reads the card data. It is blocking.

        :param vervose: If True, prints each byte.
        :return: None
        """
        card_data = self.reader.read_mifare().get_data()
        output = ""
        for byte in card_data:
            if verbose:
                print(hex(byte), end =" ")
            output = " ".join([output, hex(byte)])

        output
        self.reader.reset_i2c()
        return output

    def start(self, handler, join = False):
        """ Creates and starts the reader thread.
        :param handler: GUI handler to manage the read info.
        :param join: If it is been executed from the main of this module,
        waits for the thread to end (never ends) to end teh exection of the
        program. I prevents the program quit and kill the thread.
        :return: None
        """
        self.thread = threading.Thread(target=self.readUID, args=[handler])
        self.thread.daemon = True
        self.thread.start()
        if join:
            self.thread.join()

    def _parseUID(self):
        """ Extracts the User Identifier (UID) info from all the infomation read of the Mifare card

        :return: User Identifier (UID)
        """
        if not self.test:
            values = self._read()

        else:
            sleep(3)
            values = "0x3b 0x5c 0x3a 0x7b 0x2d 0x9a 0x8c 0x6e 0x3b 0x8c 0x9a 0x2c"
        uid = values.split(" ")[8:]
        uid = "".join(uid).replace("0x", "")
        return uid.upper()

    def readUID(self, handler):
        """ Main infinite loop. Executes the GUI handler function each time a card is read.
        :param handler: GUI handler to manage the read info.
        :return: None
        """
        while True:
            handler(self._parseUID())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        isTest = sys.argv[1]=="test"
    else:
        isTest = False

    lector = RFID(isTest)
    lector.start(print, True)
