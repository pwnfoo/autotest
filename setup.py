# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='autotest',
    version='0.0.1',
    description='Consume pagure fedmsg messages to test pull-request',
    license='GPLv2+',
    author='Sachin S. Kamath',
    author_email='sskamath96@gmail.com',
    url='https://github.com/sachinkamath/autotest',
    install_requires=['fedmsg', 'six'],
    packages=find_packages(
        exclude=('autotest.tests', 'autotest.tests.*')),
    test_suite='autotest.tests',
    entry_points="""
    [moksha.consumer]
    autotest = autotest.consumers:Autotest
    """,
)
