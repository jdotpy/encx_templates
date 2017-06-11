#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='encx_templates',
    version='0.1',
    description='Extension to Encx that provides template rendering (using Jinja2 engine)',
    author='KJ',
    author_email='<redacted>',
    url='https://github.com/jdotpy/encx_templates',
    packages=[
        'encx_templates',
    ],
    install_requires=[
        'jinja2',
        'pyyaml',
    ],
)
