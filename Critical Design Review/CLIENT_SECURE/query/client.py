import urllib.request
import json
from pprint import pprint


class Client():

    def __init__(self):
        print("Hello server")
        self.ip = "lacalhost:8082"

    def pass_query(self, query):
        return urllib.request.urlopen("http://" + self.ip + "/" + query).read()


if __name__ == "__main__":
    c = Client()
    i = c.pass_query("hello")
    data = json.loads(i)

    # with open('test.json') as f:
    #	data = json.load(f)
    # pprint(data)
    pprint(data)
