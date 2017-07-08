from distutils.core import setup

from setuptools import find_packages


# build_manpage comes from https://github.com/gabrielegiammatteo/build_manpage and it is used to build man page from
# the argparse cmdline parser in benchsuite.cli. Since it is not possible to express build-time dependencies,
# if this module is not installed in the system when installing the benchsuite.controller with pip the installation
# would fail
try:
    from build_manpage import build_manpage
    cmdclass = {'build_manpage': build_manpage}
except ImportError:
    cmdclass = {}
    print('\n#\n# WARNING! Module argparse-manpage is not installed. Generation of manpage will be skipped. To enable, '
          'download and install the module from https://github.com/gabrielegiammatteo/build_manpage\n#\n')

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
    cmdclass= cmdclass
)