import requests
import sys
import json

class HolmSecurityScannerAuthenticationClass():
    def __init__(self):
        self.session = requests.session()

    def login(self, username, password):
        return self.session.post("https://sc.holmsecurity.com/login/in", data={"username": username, "password": password, "redirect": "", "language": "en"}) 

    def getUserProfile(self):
        return json.loads(self.session.get("https://sc.holmsecurity.com/users/user/profile").text)['user']
        
class HolmSecurityScannerClass():
    def __init__(self, username, password):
        self.holm = HolmSecurityScannerAuthenticationClass()
        self.holm.login(username, password)
        self.userid = self.holm.getUserProfile()

    def getWebScan(self, id):
        return self.holm.session.get("https://sc.holmsecurity.com/scan/wruns/{}".format(id))

    def startWebScan(self, **kwargs):
        data = kwargs
        data['assets'] = kwargs['assets']
        data.update({"appliance": "-1",
                "source": 0,
                "node": "",
                "user": "{}".format(self.userid),
                "start_date": None,
               })

        response = json.loads(self.holm.session.post("https://sc.holmsecurity.com/scan/wscans/", data=json.dumps(data).replace(" ",""), headers={"Content-Type": "application/json"}).text)
        start_request = json.loads(self.holm.session.get("https://sc.holmsecurity.com/scan/start/{}/".format(response['id'])).text)
        return start_request['run']


