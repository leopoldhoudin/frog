import re
import codecs
import os.path
from setuptools import setup, find_packages


def find_version():
    with codecs.open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), f"frog/info.py"
        ),
        "r",
    ) as file:
        return re.search("__version__ = '(.*?)'", file.read()).group(
            1
        )


setup(
    name="frog",
    version=find_version(),
    description="Code examiner.",
    packages=find_packages(),
    install_requires=[],
    entry_points={"console_scripts": ["frog=frog.main:main"]},
)

