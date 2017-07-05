from distutils.core import setup

setup(
    name='benchsuite.controller',
    version='2.0.0-dev5',
    packages=['benchsuite'],
    package_dir={'': 'src'},
    url='https://github.com/benchmarking-suite/benchmarking-controller',
    license='',
    author='Gabriele Giammatteo',
    author_email='gabriele.giammatteo@eng.it',
    description='',
    install_requires=['appdirs', 'prettytable', 'paramiko', 'apache-libcloud', 'flask-restplus', 'benchsuite.core']
)