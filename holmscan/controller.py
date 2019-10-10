# -*- coding: utf-8 -*-

# python std lib
import copy
from distutils.util import strtobool
import json
import logging
import os
import re
import time

# holmscan imports
from holmscan.exceptions import HolmscanConfigException, HolmscanRemoteException
from holmscan.scan import Scan
from holmscan.webscan import Webscan

# 3rd party imports
import anyconfig
import appdirs
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
logging.getLogger("anyconfig").setLevel(logging.ERROR)


CONFIGURABLES = ["HOLMSCAN_DEBUG", "HOLMSEC_ENDPOINT", "HOLMSEC_TOKEN"]
DEFAULTS = {
    "HOLMSCAN_DEBUG": False,
    "HOLMSEC_ENDPOINT": "https://se-api.holmsecurity.com/v1",
    "HOLMSEC_TOKEN": "",
}
REQUIRED = ["HOLMSEC_ENDPOINT", "HOLMSEC_TOKEN"]
VALIDATORS = {"HOLMSEC_ENDPOINT": "^http(s)?://[a-zA-Z0-9._-]+/v[0-9]$"}
VALID_EXAMPLES = {"HOLMSEC_ENDPOINT": "example: https://se-api.holmsecurity.com/v1"}
CONFIG_EXAMPLES = {
    "HOLMSEC_ENDPOINT": "example: echo HOLMSEC_ENDPOINT: https://se-api.holmsecurity.com/v1 >> ~/.config/holmscan.yaml",
    "HOLMSEC_TOKEN": "example: export HOLMSEC_TOKEN=abcdef40charslongtokenabcdefabcdefabcdef",
}


class Controller(object):
    def __init__(self):
        """"
        Create a Controller object.
        """
        # Get super-early debugging by `export HOLMSCAN_DEBUG=1`
        if "HOLMSCAN_DEBUG" in os.environ and strtobool(
            str(os.environ["HOLMSCAN_DEBUG"])
        ):
            log.setLevel(logging.DEBUG)
            log.info(
                "Loglevel is: {0}".format(logging.getLevelName(log.getEffectiveLevel()))
            )

        # Load configuration files and environment variables
        self.conf = self._load_config()

        # Print the resulting/active configuration
        maxlen = 8 + len(max(dict(self.conf).keys(), key=len))
        for k, v in dict(self.conf).items():
            log.debug("{0} {1} {2}".format(k, "." * (maxlen - len(k)), v))

        # check for required configurables
        for k, v in dict(self.conf).items():
            if k in REQUIRED and not v:
                error = "{0} is not configured".format(k)
                example = CONFIG_EXAMPLES.get(k)
                if example:
                    error += ", " + example
                raise HolmscanConfigException(error)

        # check validity of configurables
        for k, v in VALIDATORS.items():
            if not re.match(VALIDATORS[k], self.conf[k]):
                error = "{0} is malformed".format(k)
                example = VALID_EXAMPLES.get(k)
                if example:
                    error += ", " + example
                raise HolmscanConfigException(error)

        self.session = requests.session()
        self.scan = Scan(self)
        self.webscan = Webscan(self)

        self.default_headers = {
            "Authorization": "Token {0}".format(self.conf.get("HOLMSEC_TOKEN"))
        }

    def _load_config(self):
        """
        Load configuration from configuration files and environment variables.

        Search order, latest has presedence:

          1. hard coded defaults
          2. /etc/holmscan.yaml
          3. /etc/holmscan.d/*.yaml
          4. ~/.config/holmscan.yaml
          5. ~/.config/holmscan.d/*.yaml
          6. environment variables
        """
        environ = os.environ.copy()

        log.debug("Loading configuration defaults")
        conf = copy.deepcopy(DEFAULTS)

        os.environ["XDG_CONFIG_DIRS"] = "/etc"

        site_conf_file = os.path.join(appdirs.site_config_dir("holmscan") + ".yaml")
        log.debug("Loading configuration file: {0}".format(site_conf_file))
        anyconfig.merge(
            conf,
            {
                k: v
                for k, v in dict(
                    anyconfig.load(site_conf_file, ignore_missing=True)
                ).items()
                if k in CONFIGURABLES
            },
        )

        site_conf_dir = os.path.join(
            appdirs.site_config_dir("holmscan") + ".d", "*.yaml"
        )
        log.debug("Loading configuration files: {0}".format(site_conf_dir))
        anyconfig.merge(
            conf,
            {
                k: v
                for k, v in dict(anyconfig.load(site_conf_dir)).items()
                if k in CONFIGURABLES
            },
        )

        user_conf_file = os.path.join(appdirs.user_config_dir("holmscan")) + ".yaml"
        log.debug("Loading configuration file: {0}".format(user_conf_file))
        anyconfig.merge(
            conf,
            {
                k: v
                for k, v in dict(
                    anyconfig.load(user_conf_file, ignore_missing=True)
                ).items()
                if k in CONFIGURABLES
            },
        )

        user_conf_dir = os.path.join(
            appdirs.user_config_dir("holmscan") + ".d", "*.yaml"
        )
        log.debug("Loading configuration files: {0}".format(user_conf_dir))
        anyconfig.merge(
            conf,
            {
                k: v
                for k, v in dict(anyconfig.load(user_conf_dir)).items()
                if k in CONFIGURABLES
            },
        )

        log.debug("Loading configuration from environment")
        anyconfig.merge(conf, {k: v for k, v in environ.items() if k in CONFIGURABLES})

        return conf

    def get(self, url, **kwargs):
        kwargs.setdefault("headers", {}).update(self.default_headers)

        log.debug("URL query and HTTP headers: {0}".format(kwargs))
        log.debug("Sending to {0}".format(url))

        try:
            t0 = time.time()
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HolmscanRemoteException(str(e)) from e
        finally:
            t1 = time.time()
            log.debug("Request took {:.4f} seconds".format(t1 - t0))

        return response

    def post(self, url, **kwargs):
        kwargs.setdefault("headers", {}).update(self.default_headers)

        log.debug("URL query, HTTP request body and HTTP headers: {0}".format(kwargs))
        log.debug("Sending to {0}".format(url))

        try:
            t0 = time.time()
            response = self.session.post(url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HolmscanRemoteException(str(e)) from e
        finally:
            t1 = time.time()
            log.debug("Request took {:.4f} seconds".format(t1 - t0))

        return response
