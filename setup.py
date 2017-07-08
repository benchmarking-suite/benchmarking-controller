from distutils.core import setup

from setuptools import find_packages


# hack for ReadTheDocs builds. Since the build_manpages must be downloaded from GitHub and it is done in the same
# requirements file
try:
    from build_manpage import build_manpage
    cmdclass = {'build_manpage': build_manpage}
except ImportError:
    cmdclass = {}

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