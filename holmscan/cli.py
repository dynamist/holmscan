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
    net                 Work with hosts and networks

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
    -v, --verbose       Verbose terminal output (multile -v increses verbosity)
    -V, --version       Display the version number and exit
"""

net_args = """
Usage:
    holmscan net [(asset || profile || scan)] [options] [<args> ...]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

net_asset_args = """
Usage:
    holmscan net asset list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

net_profile_args = """
Usage:
    holmscan net profile list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

net_scan_args = """
Usage:
    holmscan net scan list [(running || completed || all)] [options]
    holmscan net scan start [options] <asset> <profile>

Arguments:
    <asset>             Asset ID
    <profile>           Profile ID

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

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

    if cli_args["<command>"] == "net":
        sub_args = docopt(net_args, argv=argv)
        if sub_args["asset"]:
            sub_args = docopt(net_asset_args, argv=argv)
        elif sub_args["profile"]:
            sub_args = docopt(net_profile_args, argv=argv)
        elif sub_args["scan"]:
            sub_args = docopt(net_scan_args, argv=argv)
        else:
            extras(
                True, holmscan.__version__, [Option("-h", "--help", 0, True)], net_args
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

        if cli_args["<command>"] == "net" and sub_args.get("asset", False):
            data = c.scan.get_net_assets()
            log.debug(pformat(data))
        elif cli_args["<command>"] == "net" and sub_args.get("profile", False):
            data = c.scan.get_net_profiles()
            log.debug(pformat(data))
        elif cli_args["<command>"] == "net" and sub_args.get("scan", False):
            if sub_args["list"]:
                data = c.scan.list_net_scans()
                log.debug(pformat(data))
            elif sub_args["start"]:
                data = c.scan.start_net_scan(
                    asset=sub_args["<asset>"], profile=sub_args["<profile>"]
                )
                print(pformat(data))
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
