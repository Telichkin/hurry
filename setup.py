import os
import re
import codecs
from setuptools import (
    setup,
    find_packages,
)


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requires = [
    "docopt==0.6.2",
    "py==1.4.34"
]

tests_require = [
    "pytest",
    "pytest-cov",
]


setup(
    name="hurry",
    version=find_version("hurry", "__init__.py"),
    description="Hurry! helps you run your routine commands and scripts faster.",
    author="Roman Telichkin",
    author_email="roman@telichk.in",
    packages=find_packages(exclude=["tests"]),
    install_requires=requires,
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    entry_points="""
    [console_scripts]
    hurry=hurry.main:main
    """
)
