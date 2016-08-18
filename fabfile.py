# -*- coding: utf-8 -*-

## Fabfile application
## job application test
## key words: python, fabric, nginx, mount (fstab)
## Carlos Berton [ berton.5b@gmail.com ]

import tempfile

from fabric.api import task, env, run, cd, prefix, settings, sudo, put
from fabric.contrib.files import exists

# globals
env.project_name = 'app1'

# environments
def webserver():
    """
    Use the webserver
    """
    env.hosts = ['162.243.174.20']
    env.port = '22' # port to connect
    env.user = 'bec' # create a diferente user like deploy
    # mount partition
    env.path_mountpoint = '/data' # complete path to mounted partition
    env.path_partition = '/dev/vda' # complete path to partition to mount
    # nginx config
    env.proxy_host = 'www.google.com'
    env.server_name = '162.243.174.20'
    env.proxy_location = 'azion'
    env.access_log = '/tmp/access_log_%(project_name)s' % env
    env.error_log = '/tmp/error_log_%(project_name)s' % env
    env.page_index = 'index.html'
    env.extra_location = 'app2'
    env.extra_index = 'index.html'

def deploy():
    setup()
    if not check_nginx():
        install_nginx()
    create_and_link_site_project()
    create_index_html()
    restart_nginx()


def setup():
    """
    Setup
    """
    if not is_mounted():
        if not exists(env.path_mountpoint):
            sudo("mkdir %(path_mountpoint)s" % env)
            print "[ OK ] Diretório %(path_mountpoint)s criado." % env
        else:
            print "[ OK ] Diretório %(path_mountpoint)s existe." % env
        if env.path_partition:
            if mount().failed: # Fix me - if path_mountpoint exists and have content?
                print "[ - ] Não montado! Veja o arquivo README."
            else:
                print "[ OK ] Montado: %(path_partition)s em %(path_mountpoint)s!" % env
    else:
        print "[ OK ] Montado: %(path_partition)s em %(path_mountpoint)s!" % env


def is_mounted():
    with settings(warn_only=True):
        if run('mount -l | grep %(path_mountpoint)s' % env):
            return True
        else:
            return False


def mount():
    # mount -a
    return sudo("mount %(path_partition)s %(path_mountpoint)s" % env)


def check_nginx():
    with settings(warn_only=True):
        if sudo("which nginx"):
            return True
        else:
            return False


def install_nginx():
    """
    Install nginx
    """
    return sudo("apt-get update; apt-get install nginx")


def create_and_link_site_project():
    """
    Create configuration file to site
    """
    # todo - use upload_template
    #upload_template('configs/nginx_template.tpl','/etc/nginx/sites-available/%(project_name)s' % env, context=context, mode=0644, use_sudo=True)
    template = """# todo: consider use upstream
server {
    listen 80;
    server_name %(server_name)s;

    charset utf-8;

    root %(path_mountpoint)s;
    index %(page_index)s;

    access_log %(access_log)s;
    error_log %(error_log)s;

    location /%(project_name)s{
        try_files $uri $uri/ /index.html;
    }

    location /%(extra_location)s{
        return 301 $scheme://$server_name/%(project_name)s;
    }

    location /%(proxy_location)s/{
        proxy_pass http://%(proxy_host)s;
        proxy_redirect http://%(proxy_host)s http://%(server_name)s/%(proxy_location)s/;
    }
}""" % env

    local_path = tempfile.mktemp('')
    with open(local_path, 'w+') as output:
        output.write(template)
    put(local_path, "/etc/nginx/sites-available/%(project_name)s" % env, use_sudo=True)
    symb_link_enable_project_nginx()


def create_index_html():
    """
    Create index file to nginx
    """
    template = """<!DOCTYPE html>
<html>
<head>
    <title>%(project_name)s</title>
    <style>
    body {
        width: 35em;
        margin: 0 auto;
        font­family: Tahoma, Verdana, Arial, sans­serif;
    }
    </style>
</head>
<body>
    <h1>This is my APP: %(project_name)s!</h1>
    <p>Your APP index page can be shown.</p>
</body>
</html>"""
    local_path = tempfile.mktemp('.html')
    with open(local_path, 'w+') as output:
        output.write(template)
    put(local_path, "%(path_mountpoint)s/index.html" % env, use_sudo=True)


def symb_link_enable_project_nginx():
    """
    Symbolic links to enable projects on nginx
    """
    sudo("ln -sf /etc/nginx/sites-available/%(project_name)s /etc/nginx/sites-enabled/%(project_name)s" % env)


def start_nginx():
    """
    Start nginx
    """
    sudo("service nginx start")

    
def restart_nginx():
    """
    Restart nginx
    """
    sudo("service nginx restart")


def test_nginx():
    """
    Test configurations files for nginx
    """
    sudo("nginx -t")
