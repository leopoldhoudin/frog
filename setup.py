from codecs import open
from os.path import join
from os.path import abspath
from os.path import dirname
from re import search
from setuptools import setup, find_packages


def find_version():
    with open(join(abspath(dirname(__file__)), f'frog/info.py'), 'r') as file:
        return search("__version__ = '(.*?)'", file.read()).group(1)


setup(
    name='frog',
    version=find_version(),
    description='Code examiner.',
    packages=find_packages(),
    install_requires=['progress'],
    entry_points={'console_scripts', ['frog=frog.__main__:main']},
)

