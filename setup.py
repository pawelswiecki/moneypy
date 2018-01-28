# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='moneypy',
    version='0.0.1',
    description='Python Money type for handling currency operations.',
    long_description=readme,
    author='Paweł Święcki',
    author_email='pawel.swiecki@gmail.com',
    url='https://github.com/pawelswiecki/moneypy',
    license=license,
    packages=find_packages(exclude=('tests',))
)
