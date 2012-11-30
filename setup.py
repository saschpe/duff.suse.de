#!/usr/bin/env python

# Copyright 2012 Sascha Peilicke <saschpe@gmx.de>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
import subprocess
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="duff.suse.de",
    version="0.0.1",
    license="GPLv2",
    #description=py2pack.__doc__,
    #long_description=open('README.rst').read(),
    author="Sascha Peilicke",
    author_email="saschpe@suse.de",
    url='http://github.com/saschpe/duff.suse.de',
    #packages=['py2pack'],
    #package_data={'py2pack': ['templates/*']},
    #data_files=[('share/doc/duff.suse.de', ['LICENSE', 'README.rst']),
    #requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
