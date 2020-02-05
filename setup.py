import os
import re
import sys
from setuptools import setup, find_packages
__VERSION__ = "0.2"

sys.path.append("./src")
sys.path.append("./tests")
with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="japan_horse_racing",
    version=__VERSION__,
    description="ForecGetting the horse racing result in Japan.",
    long_description=long_description,
    author="Yusuke Kambara",
    license="MIT",

    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite = "tests.test.suite",
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "hrj=src.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ]
)