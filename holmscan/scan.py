# -*- coding: utf-8 -*-

# python std lib
import json
import logging
import re

# holmscan imports
from holmscan.exceptions import HolmscanDataException, HolmscanRemoteException
from holmscan.interface import HolmscanModule

log = logging.getLogger(__name__)


class Scan(HolmscanModule):
    def __init__(self, phabricator):
        super(Scan, self).__init__(phabricator)

    def get_secret(self, ids):
        if not self._validate_identifier(ids):
            raise HolmscanDataException('Identifier "{0}" is not valid.'.format(ids))

        ids = ids.replace("K", "")

        return response["data"]

    def kaboom(self):
        print("kaboom")
