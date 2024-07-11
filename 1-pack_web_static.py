#!/usr/bin/python3
""" Generate a .tgz archive from the contents of the web_static """

from fabric.api import *
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive """
    time = datetime.now()
    arch = 'web_static_' + time.strftime("%Y%m%d%H%M%S") + '.' + 'tgz'
    local('mkdir -p versions')
    result = local('tar -cvzf versions/{} web_static'.format(arch))
    if result is not None:
        return arch
    else:
        return None
