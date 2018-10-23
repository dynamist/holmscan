import requests
import sys
import json

class HolmSecurityWeb():
    def __init__(self, username, password):
        self.session = requests.session()
        self.login(username, password)
        self.userid = self.getUserId()

    def login(self, username, password):
        return self.session.post("https://sc.holmsecurity.com/login/in", 
                                 data={"username": username, 
                                       "password": password, 
                                       "redirect": "", 
                                       "language": "en"}) 

    def getUserId(self):
        return json.loads(self.session.get("https://sc.holmsecurity.com/users/user/profile").text)['user']
 
    def getWebScan(self, id):
        return self.session.get("https://sc.holmsecurity.com/scan/wruns/{}".format(id))

    def startWebScan(self, **kwargs):
        data = kwargs
        data['assets'] = kwargs['assets']
        data.update({"appliance": "-1",
                "source": 0,
                "node": "",
                "user": "{}".format(self.userid),
                "start_date": None,
               })

        resp = self.session.post("https://sc.holmsecurity.com/scan/wscans/", 
                                 data=json.dumps(data).replace(" ",""), 
                                 headers={"Content-Type": "application/json"})

        response = json.loads(resp.text)
        start_resp = self.session.get("https://sc.holmsecurity.com/scan/start/{}/".format(response['id']))
        start_response = json.loads(start_resp.text)
        return start_response['run']


