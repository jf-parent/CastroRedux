#!/usr/bin/env python
# -*- coding: utf-8 -*-


from distutils.core import setup, Extension

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='castroredux',
    version='0.1.5',
    description="'screencast robot' - a tiny fork of vnc2flv",
    long_description=readme,
    author="Brome-HQ",
    author_email='brome.hq@gmail.com',
    url='https://github.com/brome-hq/castroredux',
    packages=[
        'castroredux',
        'castroredux/vnc2flv'
    ],
    package_dir={'castroredux':
                 'castroredux'},
    license="ISCL",
    keywords='castroredux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    ext_modules=[Extension('flvscreen',
                         ['flvscreen/flvscreen.c'],
                         #define_macros=[],
                         #include_dirs=[],
                         #library_dirs=[],
                         #libraries=[],
                         )]
)
