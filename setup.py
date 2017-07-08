from distutils.core import setup

from setuptools import find_packages
from build_manpage import build_manpage


setup(
    name='benchsuite.controller',
    version='2.0.0-dev14',
    packages=find_packages('src'),
    namespace_packages=['benchsuite'],
    package_dir={'': 'src'},
    scripts=['src/scripts/benchsuite'],
    url='https://github.com/benchmarking-suite/benchsuite-controller',
    license='',
    author='Gabriele Giammatteo',
    data_files = [('man/man1', ['benchsuite.1'])],
    author_email='gabriele.giammatteo@eng.it',
    description='',
    install_requires=['appdirs', 'prettytable', 'paramiko', 'apache-libcloud', 'benchsuite.core'],
    cmdclass={'build_manpage': build_manpage},

    #this does not seem to work (see: https://github.com/pypa/pip/issues/2381)
    setup_requires=['argparse-manpage'],
    dependency_links = ['http://github.com/gabrielegiammatteo/build_manpage/tarball/master#argparse-manpage-0.0.1']
)