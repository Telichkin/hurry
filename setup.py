import os
import re
import codecs
from setuptools import (
    setup,
    find_packages,
)

requires = [
    "docopt==0.6.2",
    "py==1.8.0"
]

tests_require = [
    "pytest",
    "pytest-cov",
]


setup(
    name="hurry",
    version="1.1",
    description="Hurry! helps you run your routine commands and scripts faster.",
    author="Roman Telichkin",
    author_email="roman@telichk.in",
    packages=find_packages(exclude=["tests"]),
    install_requires=requires,
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    entry_points="""
    [console_scripts]
    hurry=hurry:main
    """
)
