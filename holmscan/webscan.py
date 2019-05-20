# -*- coding: utf-8 -*-

# python std lib
import json
import logging
import re

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
        headers = {
            "Authorization": "Token {0}".format(
                self.controller.conf.get("HOLMSEC_TOKEN")
            )
        }
        response = self.controller.session.get(url, headers=headers)

        log.debug("Sending to {0}".format(url))

        return response.json()

    def get_web_profiles(self):
        url = "{0}/web-scans/scan-profiles".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        headers = {
            "Authorization": "Token {0}".format(
                self.controller.conf.get("HOLMSEC_TOKEN")
            )
        }
        response = self.controller.session.get(url, headers=headers)

        log.debug("Sending to {0}".format(url))

        return response.json()

    def get_web_schedules(self):
        url = "{0}/web-scans/schedules".format(
            self.controller.conf.get("HOLMSEC_ENDPOINT")
        )
        log.debug("Sending to {0}".format(url))
        headers = {
            "Authorization": "Token {0}".format(
                self.controller.conf.get("HOLMSEC_TOKEN")
            )
        }
        response = self.controller.session.get(url, headers=headers)

        return response.json()

    def list_web_scans(self):
        url = "{0}/web-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        log.debug("Sending to {0}".format(url))
        headers = {
            "Authorization": "Token {0}".format(
                self.controller.conf.get("HOLMSEC_TOKEN")
            )
        }
        # FIXME handle pagination (see next, previous)
        payload = {"limit": 10000}

        response = self.controller.session.get(url, headers=headers, params=payload)

        return response.json()

    def start_web_scan(self, asset, profile):
        url = "{0}/web-scans".format(self.controller.conf.get("HOLMSEC_ENDPOINT"))
        headers = {
            "Authorization": "Token {0}".format(
                self.controller.conf.get("HOLMSEC_TOKEN")
            )
        }
        data = {
            "name": "Test server scan",
            "profile_uuid": profile,
            "webapp_asset_uuid": asset,
        }

        log.debug("Sending to {0}".format(url))
        log.debug("JSON data: {0}".format(data))

        response = self.controller.session.post(url, headers=headers, json=data)

        return response.json()
