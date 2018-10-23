# -*- coding: utf-8 -*-

# python std lib
import copy
from distutils.util import strtobool
import logging
import os
import re

# holmscan imports
from holmscan.exceptions import HolmscanConfigException
from holmscan import scan

# 3rd party imports
import anyconfig
import appdirs

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
logging.getLogger("anyconfig").setLevel(logging.ERROR)


CONFIGURABLES = [
    "HOLMSCAN_DEBUG",
    "HOLMSEC_PASSWORD",
    "HOLMSEC_URL",
    "HOLMSEC_USERNAME",
]
DEFAULTS = {
    "HOLMSCAN_DEBUG": False,
    "HOLMSEC_PASSWORD": "",
    "HOLMSEC_URL": "https://sc.holmsecurity.com/",
    "HOLMSEC_USERNAME": "",
}
REQUIRED = ["HOLMSEC_PASSWORD", "HOLMSEC_URL", "HOLMSEC_USERNAME"]
VALIDATORS = {"HOLMSEC_URL": "^http(s)?://[a-zA-Z0-9._-]+/$"}
VALID_EXAMPLES = {"HOLMSEC_URL": "example: https://sc.holmsecurity.com/"}
CONFIG_EXAMPLES = {
    "HOLMSEC_USERNAME": "example: export HOLMSEC_USERNAME=username@example.com",
    "HOLMSEC_URL": "example: echo HOLMSEC_URL: https://sc.holmsecurity.com/ >> ~/.config/holmscan.yaml",
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
                "Loglevel is: {}".format(logging.getLevelName(log.getEffectiveLevel()))
            )

        self.conf = self._load_config()

        maxlen = 8 + len(max(dict(self.conf).keys(), key=len))
        for k, v in dict(self.conf).items():
            log.debug("{} {} {}".format(k, "." * (maxlen - len(k)), v))

        # check for required configurables
        for k, v in dict(self.conf).items():
            if k in REQUIRED and not v:
                error = "{} is not configured".format(k)
                example = CONFIG_EXAMPLES.get(k)
                if example:
                    error += ", " + example
                raise HolmscanConfigException(error)

        # check validity of configurables
        for k, v in VALIDATORS.items():
            if not re.match(VALIDATORS[k], self.conf[k]):
                error = "{} is malformed".format(k)
                example = VALID_EXAMPLES.get(k)
                if example:
                    error += ", " + example
                raise HolmscanConfigException(error)

        self.scan = scan.Scan(self.conf)

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
        log.debug("Loading configuration file: {}".format(site_conf_file))
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
        log.debug("Loading configuration files: {}".format(site_conf_dir))
        anyconfig.merge(
            conf,
            {
                k: v
                for k, v in dict(anyconfig.load(site_conf_dir)).items()
                if k in CONFIGURABLES
            },
        )

        user_conf_file = os.path.join(appdirs.user_config_dir("holmscan")) + ".yaml"
        log.debug("Loading configuration file: {}".format(user_conf_file))
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
        log.debug("Loading configuration files: {}".format(user_conf_dir))
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
