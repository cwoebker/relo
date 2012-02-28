from fabric.api import *
from fabric.contrib.console import confirm


def test():
    local("python test.py")


def commit():
    local("git add -A")
    local("git commit")


def prepare_push():
    test()
    commit()


def deploy():
    if confirm("Ready. Push?"):
        local("git push origin master")
