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
    def kaboom(self):
        print("kaboom")
