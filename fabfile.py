## Fabfile application
## job application test
## key words: python, fabric, nginx, mount (fstab)
## Carlos Berton [ berton.5b@gmail.com ]

from fabric.api import task, env, run, cd, prefix
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
    env.path = '/data' # complete path to mounted partition
    
# Tasks
@task
def setup():
    """
    Setup
    """
    if not exists(env.path): # create and mount diretory
        pass
    pass

# Helpers
def install_nginx():
    """
    Install nginx
    """
    pass
    
def configure_nginx():
    """
    Configure nginx
    """
    pass

def symb_link_enable_project_nginx()
    """
    Symbolic links to enable projects on nginx
    """
    pass

def start_nginx():
    """
    Start nginx
    """
    pass
    
def restart_nginx():
    """
    Restart nginx
    """
    pass

def test_nginx():
    """
    Test configurations files for nginx
    """
    pass

def mount_partition():
    """
    Mount partition from /etc/fstab
    """
    pass
