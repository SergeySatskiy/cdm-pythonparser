## cdm-pythonparser [![Build Status](https://travis-ci.org/SergeySatskiy/cdm-pythonparser.svg?branch=master)](https://travis-ci.org/SergeySatskiy/cdm-pythonparser)
[cdm-pythonparser repository](https://github.com/SergeySatskiy/cdm-pythonparser) contains a source code for
a Python 2 and Python 3 extension module called `cdmpyparser`.
The module exposes a couple of functions which basically take a file with a python code or a character buffer,
parse it and provide back what is found in the code: functions, classes, global variables etc.

The module is used in the [Codimension Python IDE](http://codimension.org) to show in a structured way a
content of an arbitrary python code and for some other features however, it could be used in other projects
which need a python code retrospection.

## Python 3
The [master branch](https://github.com/SergeySatskiy/cdm-pythonparser) contains code for Python 3 (3.5/3.6 grammar is covered).

The installation of the module is supported via pip:

```shell
pip install cdmpyparser
```

If you like to have the full source code which also includes a few utilities to play with, please follow these steps:

```shell
git clone https://github.com/SergeySatskiy/cdm-pythonparser.git
cd cdm-pythonparser
make
make check
make localinstall
```

## Python 2
**Attention:** Python 2 version is not supported anymore.

The latest Python 2 supporting release is 2.0.1. Both pre-built modules and source code are available in the releases area.
Here is a link: [latest Python 2 release 2.0.1](https://github.com/SergeySatskiy/cdm-pythonparser/releases/tag/v2.0.1).

If you like to build a Python 2 module from sources please follow these steps:

```shell
cd
wget https://github.com/SergeySatskiy/cdm-pythonparser/archive/v2.0.1.tar.gz
gunzip v2.0.1.tar.gz
tar -xf v2.0.1.tar
cd cdm-pythonparser-2.0.1/
make
make localinstall
make check
```

## Usage
**Note:** the example output is provided for the Python 2 module. The module name for Python 2 is `cdmbriefparser`.
In Python 3 version the name of the module differs and is `cdmpyparser`.
The output of the Python 3 module may be slightly different because more information is extracted.
However, conceptually pretty much the same information is provided for both Python 2 and 3 implementations.

Suppose there is the following file ~/my-file.py with the following content:

```python
#!/usr/bin/python
import sys

# global variable
A = 154

class C( BaseClass ):
    " class docstring "
    @decor
    def f( arg ):
        " func doc "
        return 154
```

Then the following python session may take place:

```shell
$ python
Python 2.7.9 (default, Mar 30 2015, 11:26:35)
[GCC 4.4.7 20120313 (Red Hat 4.4.7-11)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cdmbriefparser
>>> c = cdmbriefparser.getBriefModuleInfoFromFile( "my-file.py" )
>>> print c.niceStringify()
Import[2:8:25]: 'sys'
Global[5:1:48]: 'A'
Class[7:1:7:7:63:7:21]: 'C'
Base class: 'BaseClass'
Docstring[8]: 'class docstring'
    Function[10:5:10:9:122:10:17]: 'f'
    Argument: 'arg'
    Decorator[9:6:108]: 'decor
    Docstring[11]: 'func doc'
>>> c.imports[0].what
[]
>>> c.imports[0].name
'sys'
>>>
```

See the 'cdmbriefparser.py' (Python 2) or 'cdmpyparser.py' (Python3) file for the members which are supplied along with
all the recognized items.


## Comparison to the standard pyclbr module
**Note:** the comparison results are provided for the Python 2 module. The Python 3 module yeilds pretty much the same results in terms of performance while extracts more information because the grammar was extended for Python 3.

The table below shows the comparison between the standard `pyclbr` module and
the Codimension's `cdmbriefparser` module.

| *feature* | *pyclbr* | *cdmbriefparser* |
|:----------|:--------:|:----------------:|
| Extracting coding string | N | Y |
| Extracting module docstring | N | Y |
| Extracting global variables | N | Y |
| Extracting imports | N | Y |
| Extracting top level functions | Y | Y |
| Extracting nested functions | N | Y |
| Extracting functions arguments | N | Y |
| Extracting functions docstrings | N | Y |
| Extracting functions decorators | N | Y |
| Extracting classes | Y | Y |
| Extracting base classes | Y | Y |
| Extracting class attributes | N | Y |
| Extracting class instance attributes | N | Y |
| Extracting class methods | Y | Y |
| Extracting class methods arguments | N | Y |
| Extracting nested classes | N | Y |
| Extracting classes docstrings | N | Y |
| Extracting class methods docstrings | N | Y |
| Extracting classes decorators | N | Y |
| Extracting decorators arguments | N | Y |
| Keeping the hierarchy of the classes/functions of the arbitrary depth | N | Y |
| Ability to work with partially syntactically correct files | Y (silent) | Y (error messages are provided) |
| Ability to parse python code from a file | Y | Y |
| Ability to parse python code from memory | N | Y |
| Extracting classes and functions with the same names | N | Y |
| Supported python version | ANY | Up to 2.7 (series 3 has not been tested) |
| Time to process 11365 python files (python 2.7 distribution and some third party packages). | 2 min 37 sec | 24 sec |
