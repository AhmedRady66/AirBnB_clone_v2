#!/usr/bin/python3
""" Generate a .tgz archive from the contents of the web_static """

from fabric.api import *
import os
from datetime import datetime
env.hosts = ['54.146.82.115', '54.87.179.88']


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


def do_deploy(archive_path):
    """ Fabric script (based on the file 1-pack_web_static.py) """

    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split('/')[-1]
        no_ext = file_name.split('.')[0]
        path = "/data/web_static/releases/{}/".format(no_ext)

        put(archive_path, "/tmp/")
        run('mkdir -p {}'.format(path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}web_static/* {0}'.format(path))
        run('rm -rf {}web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(path))

        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
