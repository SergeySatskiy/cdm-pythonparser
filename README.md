## cdm-pythonparser [![Build Status](https://travis-ci.org/SergeySatskiy/cdm-pythonparser.svg?branch=master)](https://travis-ci.org/SergeySatskiy/cdm-pythonparser)
[cdm-pythonparser project](https://github.com/SergeySatskiy/cdm-pythonparser) is a
Python 3 (Python 2 support is limited) extension module.
The module provided functions can take a file with a python code or a character buffer,
parse it and provide back what is found in the code: functions, classes,
global variables etc.

The module is used in the [Codimension Python IDE](http://codimension.org) to show in a structured way a
content of an arbitrary python code and for some other features however, it could be used in other projects
which need a python code retrospection.

## Python 3 Installation and Building
The [master branch](https://github.com/SergeySatskiy/cdm-pythonparser) on github contains code for Python 3 (3.5/3.6/3.7 grammar is covered).

The module can be installed using pip:

```shell
pip install cdmpyparser
```

You can also retrieve the full source code which in addition has some utilities.
In order to do that you can follow these steps:


```shell
git clone https://github.com/SergeySatskiy/cdm-pythonparser.git
cd cdm-pythonparser
make
make check
make localinstall
```

## Python 3 Usage
Suppose there is the following file ~/my-file.py with the following content:

```python
#!/bin/env python
import sys

# global variable
a = 154

class C(BaseClass):
    """Class docstring"""
    @staticmethod
    def getValue(arg):
        """Method docstring"""
        return arg + 154
```

Then the following python session may take place:

```shell
$ python
Python 3.6.2 (default, Aug  9 2017, 11:11:12)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-11)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cdmpyparser
>>> c = cdmpyparser.getBriefModuleInfoFromFile('my-file.py')
>>> print(c.niceStringify())
Import[2:8:25]: 'sys'
Global[5:1:48]: 'a'
Class[7:1:7:7:63:7:19]: 'C'
Base class: 'BaseClass'
Docstring[8]: 'Class docstring'
    Function[10:5:10:9:129:10:22]: 'getValue'
    Argument: 'arg'
    Decorator[9:6:108]: 'staticmethod
    Docstring[11]: 'Method docstring'
>>> len(c.imports)
1
>>> c.imports[0].name
'sys'
>>> c.imports[0].line
2
>>> c.imports[0].pos
8
```

**Note:** Python 3 and Python 2 modules use different names. Python 3 uses
`cdmpyparser`. Python 2 uses `cdmbriefparser`.

See the 'cdmpyparser.py' file for the members which are supplied along with
all the recognized items.


## Python 2 Installation and Building
**Attention:** Python 2 version is not supported anymore.
There will be no more Python 2 releases.

The latest Python 2 release is 2.0.1. Both pre-built modules and
source code are available in the releases area on github:
[latest Python 2 release 2.0.1](https://github.com/SergeySatskiy/cdm-pythonparser/releases/tag/v2.0.1).

To build a Python 2 module from sources please follow these steps:

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

## Python 2 Usage
Suppose there is the following file ~/my-file.py with the following content:

```python
#!/bin/env python
import sys

# global variable
a = 154

class C(BaseClass):
    """Class docstring"""
    @staticmethod
    def getValue(arg):
        """Method docstring"""
        return arg + 154
```

Then the following python session may take place:

```shell
$ python
Python 2.7.12 (default, Sep 13 2016, 16:46:03)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cdmbriefparser
>>> c = cdmbriefparser.getBriefModuleInfoFromFile('my-file.py')
>>> print c.niceStringify()
Import[2:8:25]: 'sys'
Global[5:1:48]: 'a'
Class[7:1:7:7:63:7:19]: 'C'
Base class: 'BaseClass'
Docstring[8]: 'Class docstring'
    Function[10:5:10:9:129:10:22]: 'getValue'
    Argument: 'arg'
    Decorator[9:6:108]: 'staticmethod
    Docstring[11]: 'Method docstring'
>>> len(c.imports)
1
>>> c.imports[0].name
'sys'
>>> c.imports[0].line
2
>>> c.imports[0].pos
8
```

**Note:** Python 3 and Python 2 modules use different names. Python 3 uses
`cdmpyparser`. Python 2 uses `cdmbriefparser`.

See the 'cdmbriefparser.py' file for the members which are supplied along with
all the recognized items.


## Comparison to the Standard pyclbr Module
**Note:** the comparison results are provided for the Python 2 module.
The Python 3 module yeilds pretty much the same results in terms of performance
while extracts more information because the grammar was extended for Python 3.

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

## Essential Links
- [Codimension Python IDE](http://codimension.org) home page
- [latest Python 2 release 2.0.1](https://github.com/SergeySatskiy/cdm-pythonparser/releases/tag/v2.0.1)
- [Python 3 Pypi package](https://pypi.python.org/pypi?name=cdmpyparser&:action=display) page
