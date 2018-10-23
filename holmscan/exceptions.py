# -*- coding: utf-8 -*-


class HolmscanException(Exception):
    pass


class HolmscanDataException(HolmscanException):
    pass


class HolmscanConfigException(HolmscanException):
    pass


class HolmscanRemoteException(HolmscanException):
    pass
