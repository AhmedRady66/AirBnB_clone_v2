#!/usr/bin/python3
""" Distribute an archive to your web servers """

from fabric.api import put, run, env
import os
env.hosts = ['54.146.82.115', '54.87.179.88']


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
    except Exception as e:
        print(f"Error: {e}")
        return False
