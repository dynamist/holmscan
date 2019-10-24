# -*- coding: utf-8 -*-

# python std lib
import logging

# holmscan imports
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Webscan(HolmscanModule):
    def __init__(self, controller):
        super(Webscan, self).__init__(controller)

    def get_web_assets(self):
        url = "{0}/web-scans/assets".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def get_web_profiles(self):
        url = "{0}/web-scans/scan-profiles".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def get_web_schedules(self):
        url = "{0}/web-scans/schedules".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def list_web_scans(self):
        url = "{0}/web-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        # FIXME handle pagination (see next, previous)
        query = {"params": {"limit": 10000}}
        response = self.controller.get(url, **query)
        return response.json()

    def start_web_scan(self, asset, profile):
        url = "{0}/web-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        body = {
            "json": {
                "name": "Scan via API",
                "profile_uuid": profile,
                "webapp_asset_uuid": asset,
            }
        }
        response = self.controller.post(url, **body)
        return response.json()
