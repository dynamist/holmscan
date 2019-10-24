# -*- coding: utf-8 -*-

# python std lib
import logging

log = logging.getLogger(__name__)


class HolmscanModule(object):
    def __init__(self, controller):
        self.controller = controller
