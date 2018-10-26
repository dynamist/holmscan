# -*- coding: utf-8 -*-

# python stdlib
import logging

log = logging.getLogger(__name__)


def login(fn):
    """Decorator to log in to controller.

    This enables the Controller object to delay logging in and doing any network
    connections until the time when it is needed.

    :param fn: the UnifikModule method to be decorated
    :return: function wrapped for login
    """

    def wrapped(*v, **k):
        if not v[0].controller.loggedin:
            v[0].controller._login()

        retval = fn(*v, **k)

        return retval

    return wrapped
