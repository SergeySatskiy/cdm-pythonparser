#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Unit tests for the brief python parser"""

from __future__ import print_function

import os.path
import sys

moduleDir = None
selfDir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
for name in os.listdir(selfDir):
    if 'cdmpyparser.cpython' in name:
        moduleDir = selfDir
        break
if moduleDir is None:
    upDir = os.path.dirname(selfDir[:-1])
    for name in os.listdir(upDir):
        if 'cdmpyparser.cpython' in name:
            moduleDir = upDir
            break
if moduleDir is None:
    print('The cdmpyparser is not found neither at ' + selfDir +
          ' nor at ' + upDir)
    sys.exit(1)

sys.path.insert(0, upDir)
import cdmpyparser

def main(pythonFile):
    info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
    if not info.isOK:
        print("Error parsing the file " + pythonFile)
        return 1

    print(info.niceStringify())
    return 0

# Run the unit tests
if __name__ == '__main__':
    print("Testing parser version: " + cdmpyparser.getVersion())
    print("Module location: " + cdmpyparser.__file__)

    if len(sys.argv) != 2:
        print('A python file is not provided')
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print('File not found: ' + sys.argv[1])
    sys.exit(main(sys.argv[1]))
