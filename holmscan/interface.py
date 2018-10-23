# -*- coding: utf-8 -*-

# holmscan imports
from holmscan.exceptions import HolmscanRemoteException


class HolmscanModule(object):
    def __init__(self, configuration):
        print("HOLMSEC_URL: {}".format(configuration.get("HOLMSEC_URL")))
        print("HOLMSEC_USERNAME: {}".format(configuration.get("HOLMSEC_USERNAME")))
        print("HOLMSEC_PASSWORD: {}".format(configuration.get("HOLMSEC_PASSWORD")))
