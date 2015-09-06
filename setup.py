#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='pytest-data',
    version='0.1',
    packages=['pytest_data'],

    url='https://github.com/horejsek/python-pytest-data',
    author='Michal Horejsek',
    author_email='horejsekmichal@gmail.com',
    description='Useful functions for managing data for pytest fixtures',
    license='PSF',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
