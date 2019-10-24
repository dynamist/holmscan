# -*- coding: utf-8 -*-

# python std lib
import logging

# holmscan imports
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Webscan(HolmscanModule):
    def __init__(self, controller):
        super(Webscan, self).__init__(controller)

    def get_web_scan(self, uuid):
        path = "/web-scans/{0}".format(uuid)
        response = self.controller.get(path)
        return response.json()

    def get_web_assets(self):
        path = "/web-scans/assets"
        response = self.controller.get(path)
        return response.json()

    def get_web_profiles(self):
        path = "/web-scans/scan-profiles"
        response = self.controller.get(path)
        return response.json()

    def get_web_schedules(self):
        path = "/web-scans/schedules"
        response = self.controller.get(path)
        return response.json()

    def list_web_scans(self):
        path = "/web-scans"
        # FIXME handle pagination (see next, previous)
        query = {"params": {"limit": 10000}}
        response = self.controller.get(path, **query)
        return response.json()

    def start_web_scan(self, asset, profile):
        path = "/web-scans"
        body = {
            "json": {
                "name": "Scan via API",
                "profile_uuid": profile,
                "webapp_asset_uuid": asset,
            }
        }
        response = self.controller.post(path, **body)
        return response.json()
