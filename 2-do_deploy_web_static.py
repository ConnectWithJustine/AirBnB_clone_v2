#!/usr/bin/python3
"""
    Fabric script (based on the file 1-pack....py)
    that distributes an archive to your web servers
"""

from fabric.api import *
from fabric.contrib import files
import os

env.hosts = ['3.84.237.21', '18.204.13.20']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
        Function to transfer archive_path to web server"""

    if not os.path.isfile(archive_path):
        return False

    with cd('/tmp'):
        # Extract informatin from the archive_path
        basename = os.path.basename(archive_path)
        root, ext = os.path.splitext(basename)
        outpath = '/data/web_static/releases/{}'.format(root)
        try:
            # Upload the archive to the web server's /tmp dir
            putpath = put(archive_path)

            # If the release dirctory exists, remove it
            if files.exists(outpath):
                run('rm -rdf {}'.format(outpath))

            # Crerate the release dir
            run('mkdir -p {}'.format(outpath))

            # Extract the content of the archive to the release dirctory
            run('tar -xzf {} -C {}'.format(putpath[0], outpath))

            # Remove the uploaded archive
            run('rm -f {}'.format(putpath[0]))

            # Move web_static directory to the release directory
            run('mv -u {}/web_static/* {}'.format(outpath, outpath))

            # Remove the original web_static dirctory
            run('rm -rf {}/web_static'.format(outpath))

            # Remove the existing /data/web_static/current symbol link
            run('rm -rf /data/web_static/current')

            # Create a new symbolic link pointing to the latest release
            run('ln -sf {} /data/web_static/current'.format(outpath))

            print('New version deployed!')

            run('sudo systemctl restart nginx')
        except Exception as e:
            print(e)
            return False
        else:
            return True
