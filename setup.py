import os, sys
from setuptools import setup

if 'sdist' in sys.argv:
    dir = os.getcwd()
    os.chdir(os.path.join(dir, 'rules_light'))
    os.system('django-admin compilemessages')
    os.chdir(dir)

setup()
