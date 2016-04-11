# cdm-pythonparser [![Build Status](https://travis-ci.org/SergeySatskiy/cdm-pythonparser.svg?branch=master)](https://travis-ci.org/SergeySatskiy/cdm-pythonparser)
cdm-pythonparser project is a Python 2 extension module.
It takes a file with a python code (or a character buffer), parses it and
provides back what is found in the code: functions, classes, global variables etc.

The parser is used in the Codimension Python IDE to show in a structured way a
content of an arbitrary python code.

## Building from git clone

```shell
git clone https://github.com/SergeySatskiy/cdm-pythonparser.git
cd cdm-pythonparser
make
make check
make localinstall
```


## Usage

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

See the 'cdmbriefparser.py' file for the members which are supplied along with
all the recognized items.


## Comparison to the standard pyclbr module

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

