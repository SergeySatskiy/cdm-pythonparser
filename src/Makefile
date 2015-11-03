#
# cdm-pythonparser - python 2 content parser used in Codimension to provide
# a structured view into python 2 files and character buffers
# Copyright (C) 2010-2015  Sergey Satskiy <sergey.satskiy@gmail.com>
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

.PHONY: all clean

FLAGS=-Wall -O2 -ffast-math -fomit-frame-pointer
PYTHON_INCLUDE=$(shell python -c 'import distutils.sysconfig; print distutils.sysconfig.get_python_inc()')

all: cdmpyparser.c tree.cpp
	cd .. && python setup.py build_ext --inplace
	g++ ${FLAGS} -o tree  tree.cpp -I ${PYTHON_INCLUDE} -L/opt/python-2.7/lib/ -lpython2.7

clean:
	rm -rf *.o core.* _cdmpyparser.so build/ tree

check:
	PYTHONPATH=../:${PYTHONPATH} ../tests/ut.py

localinstall:
	cd .. && python setup.py install --user

