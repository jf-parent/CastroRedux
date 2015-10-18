#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []
with open('requirements.txt', 'r') as fd:
    for line in fd:
        requirements.append(line)

setup(
    name='castroredux',
    version='0.1.1',
    description="'screencast robot' - a tiny fork of vnc2flv",
    long_description=readme,
    author="Brome-HQ",
    author_email='brome.hq@gmail.com',
    url='https://github.com/brome-hq/castroredux',
    packages=[
        'castroredux',
        'castroredux/tools',
        'castroredux/tools/vnc2flv'
    ],
    package_dir={'castroredux':
                 'castroredux'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='castroredux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
