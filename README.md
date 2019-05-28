# holmscan

A simple Python command line tool to interact with [Holm Security VMP](https://www.holmsecurity.com/vulnerability-assessment) and the [Holm Security Platform API](https://se-api.holmsecurity.com/docs/).

Example usage:

    export HOLMSEC_TOKEN=abcdef40charslongtokenabcdefabcdefabcdef

    holmscan net asset list [options]
    holmscan net profile list [options]
    holmscan net scan list [options]
    holmscan net scan start [options] <asset> <profile>

    holmscan web asset list [options]
    holmscan web profile list [options]
    holmscan web scan list [options]
    holmscan web scan start [options] <asset> <profile>

## History

The motivation to start this tool is our drive to automate all the things. So naturally we wanted to integrate vulnerability scanning as part of our CI/CD pipeline.

![Automate All the Things](https://i.imgur.com/dv5bY2Z.jpg)

We organized a hackathon at our offices and especially made it our goal to contribute to the annual [Hacktoberfest](https://hacktoberfest.digitalocean.com/). This is one of the open source tools we worked on October 23rd, 2018.

The tool has since then been updated to use the Holm Security Platform API.

## Scope

We intend to implement functionality for this tool to be able to kick off scans in an automated way. The scope is therefore limited but we may expand the scope in the future. Contributions are welcome.

## Installation in a development environment

Install the `virtualenv` and `virtualenvwrapper` software packages.

Ensure to source the correct virtualenvwrapper shell script before installing the development environment, on Ubuntu that would be `source /usr/share/virtualenvwrapper/virtualenvwrapper.sh`.

Create a virtualenv for holmscan running on Python 3.6:
```
mkvirtualenv holmscan36 --python=python3.6
```

Install code in editable mode and pull in all dependencies:
```
workon holmscan36
pip install -e '.[test]'
```

## Build and run a holmscan Docker images

Build a Docker image:
```
docker build -t holmscan .
```

Run a one-off execution:
```
docker run --rm holmscan --help
docker run --rm -e HOLMSEC_TOKEN=abcdef40charslongtokenabcdefabcdefabcdef holmscan net scan list
```

## LICENSE

Copyright (c) 2018-2019 Dynamist AB

See the LICENSE file provided with the source distribution for full details.
