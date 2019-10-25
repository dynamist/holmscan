# -*- coding: utf-8 -*-
"""
holmscan
===

A simple Python tool to interact with Holm Security VMP
"""

from __future__ import print_function

# python std library
import logging
import logging.config
import sys
from pprint import pformat

# holmscan imports
from holmscan import constants
from holmscan.controller import Controller
from holmscan.exceptions import (
    HolmscanConfigException,
    HolmscanDataException,
    HolmscanRemoteException,
)

# 3rd party imports
from docopt import docopt, extras, Option, DocoptExit
from tabulate import tabulate
import yaml


log = None

tabulate_args = {"tablefmt": "fancy_grid"}
yaml_dump_args = {"indent": 2, "sort_keys": False}
print_format = "table"

base_args = """
Usage:
    holmscan [-v ...] [options] <command> [<args> ...]

Available commands are:
    net                 Work with hosts and networks
    web                 Work with websites

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
    holmscan net scan list [(running || completed || error || all)] [options]
    holmscan net scan show <uuid> [options]
    holmscan net scan start [options] <asset> <profile>

Arguments:
    <uuid>              Scan ID
    <asset>             Asset ID
    <profile>           Profile ID

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

net_schedule_args = """
Usage:
    holmscan net schedule list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

web_args = """
Usage:
    holmscan web [(asset || profile || scan)] [options] [<args> ...]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

web_asset_args = """
Usage:
    holmscan web asset list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

web_profile_args = """
Usage:
    holmscan web profile list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

web_scan_args = """
Usage:
    holmscan web scan list [(running || completed || error || all)] [options]
    holmscan web scan show <uuid> [options]
    holmscan web scan start [options] <asset> <profile>

Arguments:
    <uuid>              Scan ID
    <asset>             Asset ID
    <profile>           Profile ID

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""

web_schedule_args = """
Usage:
    holmscan web schedule list [options]

Options:
    -h, --help          Show this help message and exit
    -q, --quiet         Suppress terminal output
"""


def _print_format(data, headers):
    if print_format == constants.OUTPUT_FORMAT_TABLE:
        print(tabulate(data, headers, **tabulate_args))
    elif print_format == constants.OUTPUT_FORMAT_YAML:
        data_with_headers = []
        for scan in data:
            scan_with_headers = {}
            for header, entry in zip(headers, scan):
                scan_with_headers[header.lower()] = entry
            data_with_headers.append(scan_with_headers)
        print(yaml.dump(data_with_headers, **yaml_dump_args))
    else:
        raise HolmscanConfigException(
            "unsupported print format: {0}".format(print_format)
        )


def _print_usage(text):
    import holmscan

    extras(True, holmscan.__version__, [Option("-h", "--help", 0, True)], text)


def parse_cli():
    """
    Parse the CLI arguments and options.
    """
    import holmscan

    global log

    try:
        cli_args = docopt(
            base_args, options_first=True, version=holmscan.__version__, help=True
        )
    except DocoptExit:
        _print_usage(base_args)

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
# FIXME add schedule functionality: T518
#        elif sub_args["schedule"]:
#            sub_args = docopt(net_schedule_args, argv=argv)
        else:
            _print_usage(net_args)
    elif cli_args["<command>"] == "web":
        sub_args = docopt(web_args, argv=argv)
        if sub_args["asset"]:
            sub_args = docopt(web_asset_args, argv=argv)
        elif sub_args["profile"]:
            sub_args = docopt(web_profile_args, argv=argv)
        elif sub_args["scan"]:
            sub_args = docopt(web_scan_args, argv=argv)
# FIXME add schedule functionality: T518
#        elif sub_args["schedule"]:
#            sub_args = docopt(web_schedule_args, argv=argv)
        else:
            _print_usage(web_args)
    else:
        _print_usage(base_args)
        sys.exit(1)

    return (cli_args, sub_args)


def run(cli_args, sub_args):
    """
    Run the CLI application.
    """
    retcode = 0

    try:
        c = Controller()

        global print_format
        print_format = c.conf["HOLMSCAN_FORMAT"]

        if cli_args["<command>"] == "net" and sub_args.get("asset", False):
            data = c.netscan.get_net_assets()
            log.debug(pformat(data))
            filtered = [[item["name"], item["uuid"]] for item in data["results"]]
            _print_format(filtered, headers=["Name", "UUID"])
        elif cli_args["<command>"] == "net" and sub_args.get("profile", False):
            data = c.netscan.get_net_profiles()
            log.debug(pformat(data))
            filtered = [[item["name"], item["uuid"]] for item in data]
            _print_format(filtered, headers=["Name", "UUID"])
        elif cli_args["<command>"] == "net" and sub_args.get("scan", False):
            if sub_args["list"]:
                data = c.netscan.list_net_scans()
                log.debug(pformat(data))
                # FIXME handle pagination (see next, previous)
                if sub_args["all"]:
                    status = constants.SCAN_STATUS_CHOICES
                elif sub_args[constants.SCAN_STATUS_COMPLETED]:
                    status = [constants.SCAN_STATUS_COMPLETED]
                elif sub_args[constants.SCAN_STATUS_ERROR]:
                    status = [constants.SCAN_STATUS_ERROR]
                else:  # default value
                    status = [constants.SCAN_STATUS_RUNNING]

                filtered = [
                    [
                        item["started_date"],
                        item["finished_date"],
                        item["status"],
                        item["vulnerabilities_count"],
                        item["uuid"],
                    ]
                    for item in data["results"]
                    if item["status"] in status
                ]
                _print_format(
                    filtered, headers=["Start", "Finished", "Status", "Vulns", "UUID"]
                )
            elif sub_args["show"]:
                data = c.netscan.get_net_scan(uuid=sub_args["<uuid>"])
                log.debug(pformat(data))
                columns = [
                    "started_date",
                    "duration",
                    "status",
                    "vulnerabilities_count",
                    "scanned_hosts",
                    "name",
                ]
                filtered = [[data[column] for column in columns]]
                _print_format(
                    filtered,
                    headers=["Start", "Duration", "Status", "Vulns", "Hosts", "Name"],
                )
            elif sub_args["start"]:
                data = c.netscan.start_net_scan(
                    asset=sub_args["<asset>"], profile=sub_args["<profile>"]
                )
                filtered = [[v] for k, v in data.items()]
                _print_format(filtered, headers=["UUID"])
# FIXME add schedule functionality: T518
#        elif cli_args["<command>"] == "net" and sub_args.get("schedule", False):
#            data = c.netscan.get_net_schedules()
#            log.debug(pformat(data))
        elif cli_args["<command>"] == "web" and sub_args.get("asset", False):
            data = c.webscan.get_web_assets()
            log.debug(pformat(data))
            filtered = [[item["name"], item["uuid"]] for item in data["results"]]
            _print_format(filtered, headers=["Name", "UUID"])
        elif cli_args["<command>"] == "web" and sub_args.get("profile", False):
            data = c.webscan.get_web_profiles()
            log.debug(pformat(data))
            filtered = [[item["name"], item["uuid"]] for item in data]
            _print_format(filtered, headers=["Name", "UUID"])
        elif cli_args["<command>"] == "web" and sub_args.get("scan", False):
            if sub_args["list"]:
                data = c.webscan.list_web_scans()
                log.debug(pformat(data))
                # FIXME handle pagination (see next, previous)
                if sub_args["all"]:
                    status = constants.SCAN_STATUS_CHOICES
                elif sub_args[constants.SCAN_STATUS_COMPLETED]:
                    status = [constants.SCAN_STATUS_COMPLETED]
                elif sub_args[constants.SCAN_STATUS_ERROR]:
                    status = [constants.SCAN_STATUS_ERROR]
                else:  # default value
                    status = [constants.SCAN_STATUS_RUNNING]
                filtered = [
                    [
                        item["started_date"],
                        item["finished_date"],
                        item["status"],
                        item["vulnerabilities_count"],
                        item["uuid"],
                    ]
                    for item in data["results"]
                    if item["status"] in status
                ]
                _print_format(
                    filtered, headers=["Start", "Finished", "Status", "Vulns", "UUID"]
                )
            elif sub_args["show"]:
                data = c.webscan.get_web_scan(uuid=sub_args["<uuid>"])
                log.debug(pformat(data))
                columns = [
                    "started_date",
                    "duration",
                    "status",
                    "vulnerabilities_count",
                    "name",
                ]
                filtered = [[data[column] for column in columns]]
                _print_format(
                    filtered, headers=["Start", "Duration", "Status", "Vulns", "Name"]
                )
            elif sub_args["start"]:
                data = c.webscan.start_web_scan(
                    asset=sub_args["<asset>"], profile=sub_args["<profile>"]
                )
                filtered = [[v] for k, v in data.items()]
                _print_format(filtered, headers=["UUID"])
# FIXME add schedule functionality: T518
#        elif cli_args["<command>"] == "web" and sub_args.get("schedule", False):
#            data = c.webscan.get_web_schedules()
#            log.debug(pformat(data))
    except (
        HolmscanConfigException,
        HolmscanDataException,
        HolmscanRemoteException,
    ) as e:
        print(e, file=sys.stderr)
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
