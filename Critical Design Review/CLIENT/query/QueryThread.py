from .http import get

class QueryThreader:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.hash_uid = None
        self.timeout = 10

    def get_username(self, uid, handler):
        """TBC
        :  handler: handler function
        :returns:  None
        """
        self.hash_uid = hash(uid)
        url = "http://" + self.ip + ':' + self.port + '/Users?uid='+self.hash_uid
        get(url, handler, None)

    def send_query(self,handler , req):
        """
        TBC
        :param handler:
        :param req:
        :return:
        """
        if '?' not in req:
            req = req+'?'
        url = "http://" + self.ip + ':' + self.port + '/' + req + '&uid='+self.hash_uid
        get(url, handler, req.split('?')[0])
        


if __name__ == '__main__':
    server = QueryThreader('localhost', '8081')
    server._http_request(print, 'test')

