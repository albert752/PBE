from gi.repository import GLib
from threading import  Thread
import requests
import Jibril


def get(url, handler, args):
        """Makes a simple request  asking for thecomplete name of the user. Also
        saves the UID vvariable for the upcoming queries. After retrieving the 
        full name, if it is valid (difrerent than []) handler ok get executed if not handler ko fets executed
        :param: uid: desired users uid
        :  handler: handler function
        :returns:  None
        """
        def target_thread(url, handler, args):
            try:
                data = requests.get(url, verify=False, timeout=10).json() 
				data = 
            except requests.exceptions.RequestException as e: 
                data = "Timeout error"
            GLib.idle_add(handler, data, args)

        thread = Thread(target=target_thread, args=[url, handler, args])
        thread.daemon = True
        thread.start()
    

