from threading import Event, Thread
from gi.repository import GLib
import requests

class QueryThreader:
    def __init__(self, ip, port):
        print("hello")
        self.ip = ip
        self.port = port
        self.uid = None
        self.timeout = 10

    def get_username(self, uid, handler_ok, handler_ko):
        """Makes a simple request  asking for thecomplete name of the user. Also
        saves the UID vvariable for the upcoming queries. After retrieving the 
        full name, if it is valid (difrerent than []) handler ok get executed if not handler ko fets executed
        :param: uid: desired users uid
        :  handler: handler function
        :returns:  None
        """
        def target_thread(uid, handler_ok, handler_ko):
            self.uid = uid
            url = "http://" + self.ip + ':' + self.port + '/Users?{"uid":"'+ uid+'"}'
            try:
                data = requests.get(url, verify=False, timeout=self.timeout).json()
            except requests.exceptions.RequestException as e: 
                data = "Timeout error"

            if data == []:
                GLib.idle_add(handler_ko, None)
            elif data == "Timeout error":
                GLib.idle_add(handler_ko, data)
            else:
                GLib.idle_add(handler_ok, data[0]['name'])

        thread = Thread(target=target_thread, args=[uid, handler_ok, handler_ko])
        thread.daemon = True
        thread.start()


    def send_query(self, req, handler):
        """Starts a thread with target _htt_request (see for more detail on parameters)
			:param: req: desired req
						:  handler: handler function
			:returns:  None
		"""
        thread = Thread(target=self._http_request, args=[req, handler])
        thread.daemon = True
        thread.start()
        thread.join()

    def _http_request(self, handler, req):
        """Makes a simple request  with req as a parameter. After retrieving the 
        response, adds the handler with parameter the json loader response to GLib
        :param: req: desired req
        :  handler: handler function
        :returns:  None
        """
        url = "http://" + self.ip + ':' + self.port + '/' + req
        url = url.replace("}", '"uid":"'+ self.uid+'"}')
        try:
            data = requests.get(url, verify=False, timeout = self.timeout).json()
        except requests.exceptions.RequestException as e: 
            data = "Timeout error"
        print(data)
        GLib.idle_add(handler, data, req.split("?")[0])


if __name__ == '__main__':
    server = QueryThreader('localhost', '8081')
    server._http_request(print, 'test')

