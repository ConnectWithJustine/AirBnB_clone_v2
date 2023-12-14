#!/usr/bin/python3
"""
    Fabric script that generates a .tgz archive"""

from fabric.api import *
from datetime import datetime as dt
import os


def do_pack():
    """ A function to create tarball of webstatic """

    # Use fabric's settings to handle warnings
    with settings(warn_only=True):
        # check if 'version' dir exits, create if not
        isdir = os.path.isdir('versions')
        if not isdir:
            mkdir = local('mkdir versions')
            if mkdir.failed:
                return None

            # Generate a timestamp for the archive filename
        suffix = dt.now().strftime('%Y%m%d%M%S')

        # Define the path for the tarball
        path = 'versions/web_static_{}.tgz'.format(suffix)

        # Create the tarball using the 'tar'
        tar = local('tar -cvzf {} web_static'.format(path))
        if tar.failed:
            return None
        size = os.stat(path).st_size
        print('web_static packed: {} -> {}Bytes'.format(path, size))
        return path
