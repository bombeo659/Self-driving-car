from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_disutils_setup(
    packages=['self-driving-car'],
    package_dir=['':'src'],
)

setup(**setup_args)
