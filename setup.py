import sys
from setuptools import setup, find_packages
from setuptools.command.install import install



class CustomInstallCmd(install):
    """
    Custom install command that before running the actual install command, download the argparse-manpage package and 
    invoke it to build the manpage from the argparse parser of the cli.
    """
    def run(self):

        #call(["pip install git+https://github.com/gabrielegiammatteo/build_manpage.git#egg=argparse-manpage"], shell=True)

        # import
        from build_manpage import build_manpage

        # define it as command
        self.distribution.cmdclass['build_manpage'] = build_manpage

        # run the command
        sys.path.insert(0, 'src/')  # add src dir to the path so build_manpage can find the cli module
        self.run_command('build_manpage')

        # run the standard install command
        # do not call do_egg_install() here because it would do an egg and not install the manpage
        # TODO: create a script to install the manpage from the egg resource (if we want to use the
        # standard do_egg_install() command
        install.run(self)



setup(
    name='benchsuite.cli',
    version='2.0.0-dev32',
    packages=find_packages('src'),
    namespace_packages=['benchsuite'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['benchsuite=benchsuite.cli.command:main'],
    },
    url='https://github.com/benchmarking-suite/benchsuite-cli',
    license='',
    author='Gabriele Giammatteo',
    data_files = [('man/man1', ['benchsuite.1'])],
    author_email='gabriele.giammatteo@eng.it',
    description='',
    install_requires=['prettytable', 'benchsuite.core'],
    cmdclass={'install': CustomInstallCmd},
    dependency_links = [
          'https://github.com/gabrielegiammatteo/build_manpage/zipball/master#egg=argparse-manpage-0.0.1'
          ],
    setup_requires = ['argparse-manpage==0.0.1']
)