# -*- coding: utf-8 -*-

# python std lib
import json
import logging
import re

# holmscan imports
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Scan(HolmscanModule):
    def __init__(self, controller):
        super(Scan, self).__init__(controller)

    def get_net_scan(self, uuid):
        url = "{0}/net-scans/{1}".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT"), uuid
        )
        response = self.controller.get(url)
        return response.json()

    def get_net_assets(self):
        url = "{0}/net-scans/assets".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def get_net_profiles(self):
        url = "{0}/net-scans/scan-profiles".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def get_net_schedules(self):
        url = "{0}/net-scans/schedules".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        response = self.controller.get(url)
        return response.json()

    def list_net_scans(self):
        url = "{0}/net-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        # FIXME handle pagination (see next, previous)
        query = {"params": {"limit": 10000}}
        response = self.controller.get(url, **query)
        return response.json()

    def start_net_scan(self, asset, profile):
        url = "{0}/net-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        body = {
            "json": {
                "name": "Scan via API",
                "included_assets": [asset],
                "profile_uuid": profile,
            }
        }
        response = self.controller.post(url, **body)
        return response.json()
