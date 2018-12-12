import threading
from gi.repository import GLib
import requests

class QueryThreader:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.uid = None

    def get_username(self, uid, handler):
		"""Makes a simple request  asking for thecomplete name of the user. Also
			saves the UID vvariable for the upcoming queries. After retrieving the 
			full name, adds the handler with parameter the name to GLib
			:param: uid: desired users uid
						:  handler: handler function
			:returns:  None
		"""
        self.uid = uid
        url = "http://" + self.ip + ':' + self.port + '/Users?uid=' + uid
        data = requests.get(url).json()
        GLib.idle_add(handler, data[0]['name'])

    def send_query(self, req, handler):
        """Starts a thread with target _htt_request (see for more detail on parameters)
			:param: req: desired req
						:  handler: handler function
			:returns:  None
		"""
        thread = threading.Thread(target=self._http_request, args=[req, handler])
        thread.daemon = True
        thread.start()

    def _http_request(self, handler, req):
		"""Makes a simple request  with req as a parameter. After retrieving the 
			response, adds the handler with parameter the json loader response to GLib
			:param: req: desired req
						:  handler: handler function
			:returns:  None
		"""
        url = "http://" + self.ip + ':' + self.port + '/' + req + "&uid=" + self.uid
        data = requests.get(url).json()
        GLib.idle_add(handler, data, req.split("?")[0])


if __name__ == '__main__':
    server = QueryThreader('localhost', '8081')
    server._http_request(print, 'test')

