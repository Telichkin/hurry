from setuptools import (
    setup,
    find_packages,
)

from hurry import __version__


requires = [
    "docopt==0.6.2",
    "py==1.4.34"
]


setup(
    name="hurry",
    version=__version__,
    description="Hurry! helps you run your routine commands and scripts faster.",
    author="Roman Telichkin",
    author_email="roman@telichk.in",
    packages=find_packages(exclude=["tests"]),
    install_requires=requires,
    setup_requires=["pytest-runner"],
    entry_points="""
    [console_scripts]
    hurry=hurry.main:main
    """
)
