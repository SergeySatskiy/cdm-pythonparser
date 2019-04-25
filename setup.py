# -*- coding: utf-8 -*-
#
# cdm-pythonparser - python 2 content parser used in Codimension to provide
# a structured view into python 2 files and character buffers
# Copyright (C) 2010-2017 Sergey Satskiy <sergey.satskiy@gmail.com>
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


from setuptools import setup, Extension
import os.path
import sys

description = 'Fast and comprehensive Python language parser. ' \
    'Written as a part of the Codimension project, this parser ' \
    'aims at pulling the most data from Python sources while ' \
    'exceeding the speed of existing parsers.'

try:
    version = os.environ['CDM_PROJECT_BUILD_VERSION']
except KeyError:
    version = 'trunk'
    if os.path.exists('cdmpyparserversion.py'):
        try:
            import cdmpyparserversion
            version = cdmpyparserversion.version
        except:
            pass

try:
    import pypandoc
    converted = pypandoc.convert_file('README.md', 'rst').splitlines()
    no_travis = [line for line in converted if 'travis-ci.org' not in line]
    long_description = '\n'.join(no_travis)

    # Pypi index does not like this link
    long_description = long_description.replace('|Build Status|', '')
except Exception as exc:
    print('pypandoc package is not installed: the markdown '
          'README.md convertion to rst failed: ' + str(exc), file=sys.stderr)
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding='utf-8') as f:
        long_description = f.read()


# install_requires=['pypandoc'] could be added but really it needs to only
# at the time of submitting a package to Pypi so it is excluded from the
# dependencies
setup(name='cdmpyparser',
      description=description,
      python_requires='>=3.5',
      long_description=long_description,
      version=version,
      author='Sergey Satskiy',
      author_email='sergey.satskiy@gmail.com',
      url='https://github.com/SergeySatskiy/cdm-pythonparser',
      license='GPLv3',
      classifiers=[
           'Development Status :: 5 - Production/Stable',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: GNU General Public License (GPL)',
           'Operating System :: POSIX :: Linux',
           'Programming Language :: C',
           'Programming Language :: Python :: 3',
           'Topic :: Software Development :: Libraries :: Python Modules'],
       platforms=['any'],
       py_modules=['cdmpyparser'],
       ext_modules=[Extension('_cdmpyparser',
                              ['src/cdmpyparser.c'],
                              extra_compile_args=['-Wno-unused', '-fomit-frame-pointer',
                                                  '-DCDM_PY_PARSER_VERSION="' + version + '"',
                                                  '-ffast-math',
                                                  '-O2',
                                                  '-std=c99'])])
