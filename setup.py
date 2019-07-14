#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import re
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open(os.path.join('w2v_tissues', '__init__.py')) as ver_file:
    for line in ver_file:
        if line.startswith('__version__'):
            version=re.sub("'", "", line[line.index("'"):])

requirements = [
    'argparse',
    'tzlocal',
    'flask',
    'flask-restplus',
    'Flask-Limiter',
    'numpy',
    'gensim',
    'scipy'
]

setup_requirements = [ ]

test_requirements = [
    'unittest2'
]

setup(
    author='Samson Fong',
    author_email='shfong@ucsd.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="WordToVectorTissues REST Server",
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='WordToVectorTissues.upper()',
    name='w2v_tissues',
    packages=find_packages(include=['w2v_tissues']),
    package_dir={'w2v_tissues': 'w2v_tissues'},
    package_data={'w2v_tissues': [ 'biggim_tissues.txt']},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shfong/w2v_tissues',
    version=version,
    zip_safe=False,
)
