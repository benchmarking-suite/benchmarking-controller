import sys
from subprocess import call
from setuptools import setup, find_packages
from setuptools.command.install import install



class CustomInstallCmd(install):
    """
    Custom install command that before running the actual install command, download the argparse-manpage package and 
    invoke it to build the manpage from the argparse parser of the cli.
    """
    def run(self):

        # download the needed package
        call(["pip install git+https://github.com/gabrielegiammatteo/build_manpage.git#egg=argparse-manpage"], shell=True)

        # import
        from build_manpage import build_manpage

        # define it as command
        self.distribution.cmdclass['build_manpage'] = build_manpage

        # run the command
        sys.path.insert(0, 'src/')  # add src dir to the path so build_manpage can find the cli module
        self.run_command('build_manpage')

        # run the standard install command
        install.run(self)



setup(
    name='benchsuite.controller',
    version='2.0.0-dev32',
    packages=find_packages('src'),
    namespace_packages=['benchsuite'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['benchsuite=benchsuite.controller.command.cli:main'],
    },
    url='https://github.com/benchmarking-suite/benchsuite-cli',
    license='',
    author='Gabriele Giammatteo',
    data_files = [('man/man1', ['benchsuite.1'])],
    author_email='gabriele.giammatteo@eng.it',
    description='',
    install_requires=['appdirs', 'prettytable', 'paramiko', 'apache-libcloud', 'benchsuite.core'],
    cmdclass={'install': CustomInstallCmd},
)