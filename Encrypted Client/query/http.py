from gi.repository import GLib
from threading import  Thread
import requests
from .Jibril import decrypt_data
from pprint import pprint as pp


def get(url, handler, args=None, key = None):
        """Makes a simple request  asking for thecomplete name of the user. Also
        saves the UID vvariable for the upcoming queries. After retrieving the 
        full name, if it is valid (difrerent than []) handler ok get executed if not handler ko fets executed
        :param: uid: desired users uid
        :  handler: handler function
        :returns:  None
        """
        def target_thread(url, handler, args=None, key=None):
            try:
                data = requests.get(url, verify=False, timeout=10).json() 
                print("The bool is " + str(key is not None))
                if key is not None:
                    pp(data)
                    data = decrypt_data(data, key)
                    pp(data)
            except requests.exceptions.RequestException as e: 
                data = "Timeout error"
            GLib.idle_add(handler, data, args)

        thread = Thread(target=target_thread, args=[url, handler, args, key])
        thread.daemon = True
        thread.start()
    

