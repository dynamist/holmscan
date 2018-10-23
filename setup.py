#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import holmscan

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.md") as f:
    README = f.read()
with open("CHANGELOG.md") as f:
    CHANGELOG = f.read()

install_requires = ["docopt", "requests"]
tests_require = []
download_url = "{}/tarball/v{}".format(
    "https://github.com/dynamist/holmscan", holmscan.__version__
)

setup(
    name=holmscan.__name__,
    version=holmscan.__version__,
    description=holmscan.__doc__,
    long_description=README + "\n\n" + CHANGELOG,
    author="Henrik Holmboe",
    author_email="henrik@dynamist.se",
    url=holmscan.__url__,
    download_url=download_url,
    zip_safe=False,  # Prevent creation of egg
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    packages=["holmscan"],
    entry_points={"console_scripts": ["holmscan = holmscan.cli:cli_entrypoint"]},
    classifiers=[
        # 'Development Status :: 1 - Planning',
        "Development Status :: 2 - Pre-Alpha",
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
    ],
    platforms=["OS Independent"],
    license="Apache License 2.0",
)
