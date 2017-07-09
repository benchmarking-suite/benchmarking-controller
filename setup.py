
from setuptools import setup, find_packages
from setuptools.command.install import install

class PreInstallScript(install):

    def run(self):
        sys.path.insert(0, 'src/')

        bm = build_manpage(self.distribution)
        bm.output = 'benchsuite.1'
        bm.parser = 'benchsuite.cli:get_options_parser'
        bm.finalize_options()
        bm.run()
        install.run(self)


try:
    from build_manpage import build_manpage
    cmdclass = {'install': PreInstallScript}
except ImportError:
    cmdclass = {}

import sys



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
    cmdclass=cmdclass
)