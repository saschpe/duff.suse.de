#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012, Sascha Peilicke <saschpe@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

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
