# -*- coding: utf-8 -*-

# python std lib
import logging

# holmscan imports
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Netscan(HolmscanModule):
    def __init__(self, controller):
        super(Netscan, self).__init__(controller)

    def get_net_scan(self, uuid):
        path = "/net-scans/{0}".format(uuid)
        response = self.controller.get(path)
        return response.json()

    def get_net_assets(self):
        path = "/net-scans/assets"
        response = self.controller.get(path)
        return response.json()

    def get_net_profiles(self):
        path = "/net-scans/scan-profiles"
        response = self.controller.get(path)
        return response.json()

    def get_net_schedules(self):
        path = "/net-scans/schedules"
        response = self.controller.get(path)
        return response.json()

    def list_net_scans(self):
        path = "/net-scans"
        # FIXME handle pagination (see next, previous)
        query = {"params": {"limit": 10000}}
        response = self.controller.get(path, **query)
        return response.json()

    def start_net_scan(self, asset, profile):
        path = "/net-scans"
        body = {
            "json": {
                "name": "Scan via API",
                "included_assets": [asset],
                "profile_uuid": profile,
            }
        }
        response = self.controller.post(path, **body)
        return response.json()
