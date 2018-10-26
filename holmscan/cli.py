# -*- coding: utf-8 -*-
"""
holmscan
===

A simple Python tool to interact with Holm Security VMP
"""

# python std library
import logging
import logging.config
import sys
from pprint import pformat

# holmscan imports
from holmscan.controller import Controller
from holmscan.exceptions import (
    HolmscanConfigException,
    HolmscanDataException,
    HolmscanRemoteException,
)

# 3rd party imports
from docopt import docopt


log = None

base_args = """
Usage:
    holmscan [-v ...] [options] <command> [<args> ...]

Available commands are:
    kaboom              Scan

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
    -v, --verbose       Verbose terminal output (multile -v increses verbosity)
    -V, --version       Display the version number and exit
"""

kaboom_args = """
Usage:
    holmscan kaboom [options] <asset>

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""


def parse_cli():
    """
    Parse the CLI arguments and options.
    """
    import holmscan

    global log

    from docopt import extras, Option, DocoptExit

    try:
        cli_args = docopt(
            base_args, options_first=True, version=holmscan.__version__, help=True
        )
    except DocoptExit:
        extras(True, holmscan.__version__, [Option("-h", "--help", 0, True)], base_args)

    argv = [cli_args["<command>"]] + cli_args["<args>"]

    holmscan.init_logging(1 if cli_args["--quiet"] else cli_args["--verbose"])

    log = logging.getLogger(__name__)

    log.debug(sys.argv)
    log.debug("Setting verbose level: {0}".format(cli_args["--verbose"]))
    log.debug("Arguments from CLI: \n{0}".format(pformat(cli_args)))

    if cli_args["<command>"] == "kaboom":
        sub_args = docopt(
            eval("{sub}_args".format(sub=cli_args["<command>"])), argv=argv
        )
    else:
        extras(True, holmscan.__version__, [Option("-h", "--help", 0, True)], base_args)
        sys.exit(1)

    return (cli_args, sub_args)


def run(cli_args, sub_args):
    """
    Run the CLI application.
    """
    retcode = 0

    try:
        c = Controller()

        if cli_args["<command>"] == "kaboom":
            asset = c.scan.get_asset_id(sub_args["<asset>"])
            scan_id = c.scan.start_web_scan(
                name="{0} Job".format(sub_args["<asset>"]),
                schedule_is_active=False,
                node_source_overrides=False,
                is_was_discovery=True,
                assets=[asset],
                scheduled=False,
            )
            print(c.scan.get_web_scan(scan_id))

    except (
        HolmscanConfigException,
        HolmscanDataException,
        HolmscanRemoteException,
    ) as e:
        print(e)
        retcode = 1

    return retcode


def cli_entrypoint():
    """
    Used by setup.py to create a cli entrypoint script
    """
    cli_args, sub_args = parse_cli()

    try:
        sys.exit(run(cli_args, sub_args))
    except Exception:
        raise
