import setuptools


setuptools.setup(
    name="hurry",
    version="1.1",
    description="Hurry! helps you run your routine commands and scripts faster.",
    author="Roman Telichkin",
    author_email="roman@telichk.in",
    packages=setuptools.find_packages(exclude=["tests"]),
    url="https://github.com/Telichkin/hurry",
    license="MIT",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    entry_points="""
    [console_scripts]
    hurry=hurry:main
    """
)
