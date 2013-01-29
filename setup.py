import os, sys
from setuptools import setup, find_packages, Command


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class RunTests(Command):
    description = "Run the django test suite from the testproj dir."

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        this_dir = os.getcwd()
        testproj_dir = os.path.join(this_dir, "test_project")
        os.chdir(testproj_dir)
        sys.path.append(testproj_dir)
        from django.core.management import execute_manager
        os.environ["DJANGO_SETTINGS_MODULE"] = 'test_project.settings'
        settings_file = os.environ["DJANGO_SETTINGS_MODULE"]
        settings_mod = __import__(settings_file, {}, {}, [''])
        execute_manager(settings_mod, argv=[
            __file__, "test", "rules_light"])
        os.chdir(this_dir)


setup(
    name='django-rules-light',
    version='0.0.6',
    description='Rule registry for django',
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='http://github.com/yourlabs/django-rules-light',
    packages=find_packages(),
    cmdclass={'test': RunTests},
    include_package_data=True,
    zip_safe=False,
    long_description=read('README.rst'),
    license='MIT',
    keywords='django security rules acl rbac',
    install_requires=[
        'django',
        'django-classy-tags',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
