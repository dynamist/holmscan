# -*- coding: utf-8 -*-

# python std lib
import json
import logging
import re

# holmscan imports
from holmscan.decorators import login
from holmscan.exceptions import HolmscanDataException, HolmscanRemoteException
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Scan(HolmscanModule):
    def __init__(self, controller):
        super(Scan, self).__init__(controller)

    @login
    def get_web_scan(self, id):
        url = u"{0}scan/wruns/{1}".format(self.controller.conf.get("HOLMSEC_URL"), id)

        response = self.controller.session.get(url).text

        return response

    @login
    def start_web_scan(self, **kwargs):
        data = kwargs
        data["assets"] = kwargs["assets"]
        data.update(
            {
                "appliance": "-1",
                "source": 0,
                "node": "",
                "user": "{0}".format(self.user_id),
                "start_date": None,
            }
        )

        job_url = u"{0}scan/wscans/".format(self.controller.conf.get("HOLMSEC_URL"))
        job_response = self.controller.session.post(
            job_url,
            data=json.dumps(data).replace(" ", ""),
            headers={"Content-Type": "application/json"},
        )

        job_id = json.loads(job_response.text)["id"]
        start_url = u"{0}scan/start/{1}/".format(
            self.controller.conf.get("HOLMSEC_URL"), job_id
        )
        start_response = self.controller.session.get(start_url)
        return json.loads(start_response.text)["run"]

    @login
    def get_asset_id(self, name):
        """Return the ID of an asset.

        This method first tries normal assets, then tries webapp assets.
        """
        assets_url = u"{0}assets/assets/".format(
            self.controller.conf.get("HOLMSEC_URL")
        )
        assets = json.loads(self.controller.session.get(assets_url).text)
        for asset in assets["results"]:
            # TODO: is case insensitive a good thing for asset names?
            if name.lower() == asset["name"].lower():
                return asset["id"]

        webapps_url = u"{0}scan/webapps/".format(
            self.controller.conf.get("HOLMSEC_URL")
        )
        webapps = json.loads(self.controller.session.get(webapps_url).text)
        for webapp in webapps["results"]:
            if name == webapp["name"]:
                return webapp["asset"]["id"]

        return None

    @property
    def user_id(self):
        """Return the ID of the currently logged in user."""
        url = u"{0}users/user/profile".format(self.controller.conf.get("HOLMSEC_URL"))

        # TODO properly handle if we are not logged in
        response = json.loads(self.controller.session.get(url).text)["user"]

        return response
