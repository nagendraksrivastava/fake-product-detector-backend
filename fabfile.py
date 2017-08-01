"""
Run to deply the changes.

    fab local deploy

If something is wrong then you can rollback to the previous version.

    fab local rollback

Note that this only allows you to rollback to the release immediately before
the latest one. If you want to pick a arbitrary release then you can use the
following, where 20090727170527 is a timestamp for an existing release.

    fab local deploy_version:20090727170527

"""
from fabric.api import *
from fabric.contrib.console import confirm
import time
import os

# globals
env.git_branch = 'master'
env.user = 'ubuntu'
env.project_name = 'fake-product-detector'
env.app_name = 'super_detector'
env.path = '/opt/fake-product-detector'
env.release = time.strftime('%Y%m%d%H%M%S')
env.use_shell = False
env.name_time = time.strftime('%Y-%m-%d-%H-%M')
env.local_home = os.getenv('HOME')

# CHANGE THESE DETAILS TO SUIT YOUR SYSTEM
#env.local_backup = os.path.join(env.local_home, '.tmp/sqls/') # LOCAL DB BACKUP
#env.local_sshkeys_folder = os.path.join(env.local_home, '.ssh/notiphi/') # LOCAL SSH KEYS FOLDER
env.local_sshkeys_folder = os.path.join(env.local_home, '/Users/nagendrasrivastava/counterfit-detector/server-key/') # LOCAL SSH KEYS FOLDER

def old_production():
    require('local_sshkeys_folder')
    env.key_filename = os.path.join(env.local_sshkeys_folder, "Notikum_US_WEST.pem")
    env.hosts = ['ec2-54-214-165-53.us-west-2.compute.amazonaws.com']
    env.level = 'old-prod'

def production():
    require('local_sshkeys_folder')
    env.key_filename = os.path.join(env.local_sshkeys_folder, "NotiphiRedis.pem")
    env.hosts = ['www.notiphi.com']
    env.level = 'production'

def staging():
    require('local_sshkeys_folder')
    env.key_filename = os.path.join(env.local_sshkeys_folder, "NotiphiRedis.pem")
    env.hosts = ['54.218.162.48']
    env.level = 'new-staging'

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment
    """
    require('hosts')
    require('path')
    require('project_name')

    sudo('mkdir -p %(path)s' % env)
    sudo('chown ubuntu %(path)s' % env)
    with cd('%(path)s' % env):
        run('mkdir releases; mkdir shared; mkdir packages;')


def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, install the virtual host and
    then restart the webserver
    """
    require('hosts')
    require('path')

    upload_tar_from_git()
    symlink_current_release()
    migrate()
    restart_webserver()


def deploy_version(release):
    "Specify a specific version to be made live"

    env.release = release

    with settings(warn_only=True):  # previous might not exist if done first time
        with cd('%(path)s' % env):
            run('rm releases/previous;')

    with cd('%(path)s' % env):
        run('mv releases/current releases/previous;')
    with cd('%(path)s/releases' % env):
        run('ln -s %(release)s current' % env)

    restart_webserver()


def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    Previous softlink link must exist for this to happen
    """

    with cd('%(path)s' % env):
        run('mv releases/current releases/_previous; mv releases/previous releases/current; mv releases/_previous releases/previous')
    restart_webserver()

# Helpers. These are called by other functions rather than directly


def upload_tar_from_git():
    require('release')
    require('path')

    "Create an archive from the current Git master branch and upload it"
    with settings(warn_only=True):
        run('rm -fR /tmp/%(project_name)s' % env)

    run('git clone -b %(git_branch)s https://nagendrasrivastava@bitbucket.org/nagendrasrivastava/fake-product-detector.git /tmp/%(project_name)s' % env)
    with cd('/tmp/%(project_name)s' % env):
        run('git submodule init')
        run('git submodule update')

    run('mkdir -p %(path)s/releases/%(release)s' % env)
    run('mv /tmp/%(project_name)s/* %(path)s/releases/%(release)s/' % env)

def symlink_current_release():
    "Symlink our current release"
    require('release')
    with settings(warn_only=True):
        with cd('%(path)s' % env):
            run('rm releases/previous')

    with settings(warn_only=True):
        with cd('%(path)s' % env):
            run('mv releases/current releases/previous')

    with cd('%(path)s/releases' % env):
        run('ln -s %(release)s current' % env)
    # make sure ownerships are normal
    #sudo('chown -R ubuntu:ubuntu /opt/notiphi')


def migrate():
    "Update the database"
    require('app_name')
    with cd('%(path)s/releases/current/%(app_name)s' % env):
        run('python manage.py makemigrations')
        run('python manage.py migrate')


def start_webserver():
    """Starts gunicorn using its own config file"""
    with cd('%(path)s/releases/current/%(app_name)s' % env):
        run('gunicorn_django --config %(path)s/releases/current/config/gunicorn.conf' % env)


def stop_webserver():
    sudo('kill -9 `cat /opt/fake-product-detector/shared/notiphi.pid`')


def restart_webserver():
    "Restart gunicorn by sending signal HUP"
    #sudo('kill -HUP `cat /opt/notiphi/shared/notiphi.pid`')
    stop_webserver()
    start_webserver()


#def db_backup():
 #   require('hosts')
  #  require('name_time')

#    with cd('/home/ubuntu/db_backups/'):
 #       run('mysqldump -uroot -pcapience dashboarddb > %(name_time)s.sql' % env)


#def download_db():
    '''Download database from server into local_backup'''
 #   require('hosts')
  #  require('name_time')
    # host
   # run('mysqldump -uroot -pcapience dashboarddb > %(name_time)s-%(level)s.sql' % env)
    #run('tar cfz %(name_time)s-db.tar.gz %(name_time)s-%(level)s.sql' % env)
    #with lcd(env.local_backup):
     #   get('%(name_time)s-db.tar.gz' % env, '.')
      #  run('rm %(name_time)s-%(level)s.sql' % env)
       # run('mv %(name_time)s-db.tar.gz db_backups/' % env)
        # local
        #local('tar xfz %(name_time)s-db.tar.gz' % env)
        #local('rm %(name_time)s-db.tar.gz' % env)

#def download_offer_images():
 #   require('hosts')
    # host
  #  with cd('/opt/notiphi/shared/uploaded/offer_images/'):
   #     run('tar cfz offer-images.tar.gz *')
    #    run('mv offer-images.tar.gz /home/ubuntu/')
    #with lcd(env.local_backup):
     #   get('offer-images.tar.gz', '.')
      #  run('rm offer-images.tar.gz')
