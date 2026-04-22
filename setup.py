import os, sys, subprocess
from setuptools import setup

if 'sdist' in sys.argv:
    subprocess.run(
        ['django-admin', 'compilemessages'],
        check=True,
        cwd=os.path.join(os.path.dirname(__file__), 'rules_light'),
    )

setup()
