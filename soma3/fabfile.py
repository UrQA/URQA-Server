from __future__ import with_statement
from fabric.api import local, settings, run, cd, env, prefix
from fabric.contrib.console import confirm
from fabric.contrib.files import exists
from fabric.operations import prompt, put

env.run = local
env.directory = '/home/URQA-Server'
env.activate = 'source ~/.virtualenvs/urqa/bin/activate'


def config():
    env.config_file = prompt(
        'where is global config file: ',
        default='~/Documents/config.cfg')
    env.google_file = prompt(
        'where is google config file: ',
        default='~/Documents/google_client_secrets.json')
    env.db_config_file = prompt(
        'where is db config file: ',
        default='~/Documents/dbconfig.cfg')

    with prefix(env.activate):
        with cd(env.directory):
            if not exists('/data/etc/urqa.io/'):
                run('mkdir -p /data/etc/urqa.io')
            put(env.config_file, '/data/etc/urqa.io/config.cfg')
            put(env.google_file,
                '/data/etc/urqa.io/google_client_secrets.json')
            put(env.dbconfig, '/data/etc/urqa.io/dbconfig.cfg')


def test():
    local("./manage.py test")


def deploy():
    with prefix(env.activate):
        with cd(env.directory):
            run('git checkout develop')
            run('git pull')
            install()


def setting():
    pip()
    git()
    code_dir = '~/.virtualenvs/urqa'
    with settings(warn_only=True):
        if run('test -d %s' % code_dir).failed:
            run('pip install virtualenv virtualenvwrapper')
            run('echo "source /usr/local/bin/virtualenvwrapper.sh">>~/.bashrc')
            run('export WORKON_HOME=$HOME/.virtualenvs')
            run('source ~/.bashrc')
            run('source /usr/local/bin/virtualenvwrapper.sh' +
                '&& mkvirtualenv urqa')
            run('source /usr/local/bin/virtualenvwrapper.sh && workon urqa')
        run('apt-get install -y python-dev libmysqlclient-dev')

        if run('test -d %s' % env.directory).failed:
                run('''git clone \
                    https://github.com/bongster/URQA-Server.git \
                    %s''' % env.directory)


def git():
    with settings(warn_only=True):
        result = run('git --version')
        if (result.failed and
           confirm('git are not exists, did you install git?')):
            run('apt-get install git')


def pip():
    with settings(warn_only=True):
        result = run('pip --version')
        if (result.failed and
           confirm('pip are not exists, did you install pip?')):
            run('apt-get install python-pip')


def nginx():
    run('sudo apt-get update')
    run('apt-get install nginx')


def install():
    with prefix(env.activate):
        with cd(env.directory):
            run('pip install -r requirements.txt')


def uwsgi():
    local('uwsgi --ini soma3_uwsgi.ini --static-map /static=static')


def runserver():
    env.run('python manage.py runserver 0.0.0.0:9000')
