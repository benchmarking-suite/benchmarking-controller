from subprocess import call

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.bdist_egg import bdist_egg

class PreInstallScript(install):

    def run(self):
        sys.path.insert(0, 'src/')
        call(["pip install git+https://github.com/gabrielegiammatteo/build_manpage.git#egg=argparse-manpage"], shell=True)

        from build_manpage import build_manpage
        bm = build_manpage(self.distribution)
        bm.output = 'benchsuite.1'
        bm.parser = 'benchsuite.commands.argument_parser:get_options_parser'
        bm.finalize_options()
        bm.run()
        install.run(self)

cmdclass = {'install': PreInstallScript}

import sys



setup(
    name='benchsuite.controller',
    version='2.0.0-dev27',
    packages=find_packages('src'),
    namespace_packages=['benchsuite'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['benchsuite=benchsuite.commands.cli:main'],
    },
    url='https://github.com/benchmarking-suite/benchsuite-controller',
    license='',
    author='Gabriele Giammatteo',
    data_files = [('man/man1', ['benchsuite.1'])],
    author_email='gabriele.giammatteo@eng.it',
    description='',
    install_requires=['appdirs', 'prettytable', 'paramiko', 'apache-libcloud', 'benchsuite.core'],
    cmdclass=cmdclass,
)