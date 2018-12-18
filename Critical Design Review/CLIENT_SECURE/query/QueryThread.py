from .http import get
import hashlib

class QueryThreader:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.hash_uid = None
        self.uid = None
        self.timeout = 10 # in minutes

    def get_username(self, uid, handler, secure):
        """TBC
        :  handler: handler function
        :returns:  None
        """
        print("This is the uid" + uid)
        self.hash_uid = str(hashlib.sha256(uid.encode("UTF-8")).hexdigest())
        self.uid =uid
        if secure:
            url = "http://" + self.ip + ':' + self.port + '/Secure_Users?uid='+self.hash_uid
        else:
            url = "http://" + self.ip + ':' + self.port + '/Users?uid='+self.uid
        get(url, handler, key=self.uid)

    def send_query(self,handler , req, secure):
        """
        TBC
        :param handler:
        :param req:
        :return:
        """
        if '?' not in req:
            req = req+'?'
        if secure:
            url = "http://" + self.ip + ':' + self.port + '/' + req + '&uid='+self.hash_uid
        else:
            url = "http://" + self.ip + ':' + self.port + '/' + req + '&uid='+self.uid
        
        get(url, handler, args=req.split('?')[0], key=self.uid)



if __name__ == '__main__':
    server = QueryThreader('localhost', '8081')
    server._http_request(print, 'test')

