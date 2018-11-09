from RFID import RFID
import threading
from gi.repository import GLib

def startReader(handler, isTest, join = False):
    """ Creates and starts the reader thread.
    :param handler: GUI handler to manage the read info.
    :param join: If it is been executed from the main of this module,
    waits for the thread to end (never ends) to end teh exection of the
    program. I prevents the program quit and kill the thread.
    :return: None
    """
    thread = threading.Thread(target=readUID, args=[handler, isTest])
    thread.daemon = True
    thread.start()
    if join:
        thread.join()

def readUID(handler, isTest):
    """ Main infinite loop. Executes the GUI handler function each time a card is read.
    :param handler: GUI handler to manage the read info.
    :return: None
    """
    lector = RFID(isTest)
    while True:
        GLib.idle_add(handler, lector.readUID())
