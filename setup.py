#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

NAME = 'node-checker'
DESCRIPTION = 'Simple command line tool to check if a service is online.'
URL = ''
EMAIL = 'info@dwellir.com'
AUTHOR = 'Joakim Nyman'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = None
LICENSE = 'MIT'
REQUIRED = [
    'pdpyras>=4.3.0'
]

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

about = {}
if not VERSION:
    with open(os.path.join(here, 'nodechecker', '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=['nodechecker', 'nodechecker.*']),
    entry_points={
        'console_scripts': ['node-checker=nodechecker.check:main'],
    },
    include_package_data=True,
    install_requires=REQUIRED,
    license=LICENSE,
    project_urls={ 
        'Bug Reports': '',
        'Source': '',
    },
)
