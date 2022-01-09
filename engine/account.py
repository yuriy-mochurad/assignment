# -*- coding: utf-8 -*-


def default_account():
    """
    Sets a structure for user acount
    :return (dict): default state of new user account
    """
    return {"available": 0, "held": 0, "total": 0, "locked": False}
