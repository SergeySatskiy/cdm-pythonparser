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


# The python-config is not a very reliable choice to get the compiler
# flags information. The name may depend from an interpreter version, e.g. it
# could be python3-config or it could be picked system wide but not from a
# virtual environment. So instead a python interpreter itself is used.

PYTHON_INCLUDE=$(shell python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_python_inc())')
PYTHON_LIBS_PATH=$(shell python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_config_var("LIBDIR"))')
FLAGS=-Wall -O2 -ffast-math -fomit-frame-pointer

# MacOS g++ does not like -rpath ...
OS_NAME=$(shell uname -s)
ifeq ($(OS_NAME),Linux)
FLAGS += -Wl,-rpath=${PYTHON_LIBS_PATH}
endif

# Typical python-config --ldflags output:
# -lpython3.5m -lpthread -ldl -lutil -lm -Xlinker -export-dynamic

# This will produce: -Xlinker -export-dynamic
LINK_FOR_SHARED=$(shell python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_config_var("LINKFORSHARED"))')

# This will produce: -lpthread -ldl  -lutil
LIBS=$(shell python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_config_var("LIBS"))')

# This will produce: -L. -lpython3.5m
BLD_LIBRARY=$(shell python -c 'import distutils.sysconfig; print(distutils.sysconfig.get_config_var("BLDLIBRARY"))')


all: cdmpyparser.c
	cd .. && python setup.py build_ext --inplace

tree: tree.cpp
	g++ ${FLAGS} -o tree  tree.cpp -I${PYTHON_INCLUDE} -L${PYTHON_LIBS_PATH} ${BLD_LIBRARY} ${LIBS} ${LINK_FOR_SHARED}

clean:
	rm -rf *.o core.* _cdmpyparser.so build/ tree

check:
	PYTHONPATH=../:${PYTHONPATH} ../tests/ut.py

localinstall:
	cd .. && python setup.py install --user
