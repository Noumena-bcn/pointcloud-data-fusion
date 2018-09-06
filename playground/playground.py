# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup (
    name='src',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    Developer_mail='starsk@noumena.io',
    url='https://noumena.io/downloads',
    license=license,
    packages=find_packages(exclude='src')
)

