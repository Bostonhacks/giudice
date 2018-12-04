# SPDX-License-Identifier: GPL-3.0+
from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='giudice',
    version='2.0',
    description='A judging app for hackathons',
    author='BostonHacks',
    author_email='srieger@bu.edu',
    license='GPLv3+',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
)