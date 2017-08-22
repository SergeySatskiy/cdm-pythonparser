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

import unittest
import os.path
import sys
import cdmpyparser


def files_equal(name1, name2):
    """Compares two files. Returns True if their content matches"""

    if not os.path.exists(name1):
        print("Cannot open " + name1, file=sys.stderr)
        return False

    if not os.path.exists(name2):
        print("Cannot open " + name2, file=sys.stderr)
        return False

    file1 = open(name1)
    file2 = open(name2)
    content1 = file1.read()
    content2 = file2.read()
    file1.close()
    file2.close()
    return content1.strip() == content2.strip()


class CDMBriefParserTest(unittest.TestCase):

    """Unit test class"""

    def setUp(self):
        """Initialisation"""

        self.dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
        if not os.path.isdir(self.dir):
            raise Exception("Cannot find directory with tests. "
                            "Expected here: " + self.dir)

    def meat(self, pythonFile, errorMsg):
        """The test process meat"""
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if not info.isOK:
            self.fail("Error parsing the file " + pythonFile +
                      ". Option: directly from a file.")

        f = open(pythonFile)
        content = f.read()
        f.close()

        info = cdmpyparser.getBriefModuleInfoFromMemory(content)
        if not info.isOK:
            self.fail("Error parsing the file " + pythonFile +
                      ". Option: from memory.")

        outFileName = pythonFile.replace(".py", ".out")
        outFile = open(outFileName, "w")
        outFile.write(info.niceStringify())
        outFile.close()

        okFileName = pythonFile.replace(".py", ".ok")
        if not files_equal(outFileName, okFileName):
            self.fail(errorMsg)

    def test_empty(self):
        """Test empty file"""
        self.meat(self.dir + "empty.py",
                  "empty file test failed")

    def test_import(self):
        """Tests imports"""
        self.meat(self.dir + "import.py",
                  "import test failed")

    def test_coding1(self):
        """Test coding 1"""
        self.meat(self.dir + "coding1.py",
                  "error retrieving coding")

    def test_coding2(self):
        """Test coding 2"""
        self.meat(self.dir + "coding2.py",
                  "error retrieving coding")

    def test_coding3(self):
        """Test coding 3"""
        self.meat(self.dir + "coding3.py",
                  "error retrieving coding")

    def test_function_definitions(self):
        """Test function definitions"""
        self.meat(self.dir + "func_defs.py",
                  "function definition test failed")

    def test_nested_func_definitions(self):
        """Test nested functions definitions"""
        self.meat(self.dir + "nested_funcs.py",
                  "nested functions definitions test failed")

    def test_globals(self):
        """Test global variables"""
        self.meat(self.dir + "globals.py",
                  "global variables test failed")

    def test_class_definitions(self):
        """Test class definitions"""
        self.meat(self.dir + "class_defs.py",
                  "class definitions test failed")

    def test_nested_classes(self):
        """Test nested classes"""
        self.meat(self.dir + "nested_classes.py",
                  "nested classes test failed")

    def test_docstrings(self):
        """Test docstrings"""
        self.meat(self.dir + "docstring.py",
                  "docstring test failed")

    def test_docstrings2(self):
        """Test docstrings 2"""
        self.meat(self.dir + "docstring2.py",
                  "docstring test failed (the only file content)")

    def test_docstrings3(self):
        """Test docstrings 3"""
        self.meat(self.dir + "docstring3.py",
                  "docstring test failed (many literal parts)")

    def test_decorators(self):
        """Test decorators"""
        self.meat(self.dir + "decorators.py",
                  "decorators test failed")

    def test_static_members(self):
        """Test class static members"""
        self.meat(self.dir + "static_members.py",
                  "class static members test failed")

    def test_class_members(self):
        """Test class members"""
        self.meat(self.dir + "class_members.py",
                  "class members test failed")

    def test_annotations(self):
        """Test class members"""
        self.meat(self.dir + "annot.py",
                  "annotations test failed")

    def test_errors(self):
        """Test errors"""
        pythonFile = self.dir + "errors.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if info.isOK:
            self.fail("Expected parsing error for file " + pythonFile +
                      ". Option: directly from file.")

        outFileName = pythonFile.replace(".py", ".out")
        outFile = open(outFileName, "w")
        outFile.write(info.niceStringify())
        for item in info.errors:
            outFile.write("\n" + item)
        outFile.close()

        okFileName = pythonFile.replace(".py", ".ok")
        if not files_equal(outFileName, okFileName):
            self.fail("errors test failed")

    def test_wrong_indent(self):
        """Test wrong indent"""
        pythonFile = self.dir + "wrong_indent.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if info.isOK:
            self.fail("Expected parsing error for file " + pythonFile +
                      ". Option: directly from file.")

        outFileName = pythonFile.replace(".py", ".out")
        outFile = open(outFileName, "w")
        outFile.write(info.niceStringify())
        for item in info.errors:
            outFile.write("\n" + item)
        outFile.close()

        okFileName = pythonFile.replace(".py", ".ok")
        if not files_equal(outFileName, okFileName):
            self.fail("wrong indent test failed")

    def test_wrong_stop(self):
        """Test wrong stop of the parser"""
        pythonFile = self.dir + "wrong_stop.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if info.isOK:
            self.fail("Wrong stop test failed. Expected error. Option: "
                      "directly from file " + pythonFile)

        outFileName = pythonFile.replace(".py", ".out")
        outFile = open(outFileName, "w")
        outFile.write(info.niceStringify())
        for item in info.errors:
            outFile.write("\n" + item)
        for item in info.lexerErrors:
            outFile.write("\n" + item)
        outFile.close()

        okFileName = pythonFile.replace(".py", ".ok")
        if not files_equal(outFileName, okFileName):
            self.fail("wrong stop of the parser test failed")

    def test_print(self):
        """Test print statements"""
        pythonFile = self.dir + "print.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if not info.isOK:
            outFileName = pythonFile.replace(".py", ".out")
            outFile = open(outFileName, "w")
            for item in info.errors:
                outFile.write("\n" + item)
            for item in info.lexerErrors:
                outFile.write("\n" + item)
            outFile.close()
        if not info.isOK:
            self.fail("print statement test failed")

    def test_print_func(self):
        """Test print statements"""
        pythonFile = self.dir + "print2.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if not info.isOK:
            outFileName = pythonFile.replace(".py", ".out")
            outFile = open(outFileName, "w")
            for item in info.errors:
                outFile.write("\n" + item)
            for item in info.lexerErrors:
                outFile.write("\n" + item)
            outFile.close()
        if not info.isOK:
            self.fail("Error testing the print function")

    def test_one_comment(self):
        """Test for a file which consists of a single comment line"""
        self.meat(self.dir + "one_comment.py",
                  "one comment line test failed")

    def test_comments_only(self):
        """Test for a file with no other lines except of comments"""
        self.meat(self.dir + "commentsonly.py",
                  "comments only with no other empty lines test failed")

    def test_noendofline(self):
        """Test for a file which has no EOL at the end"""
        self.meat(self.dir + "noendofline.py",
                  "No end of line at the end of the file test failed")

    def test_empty_brackets(self):
        """Test for empty brackets"""
        self.meat(self.dir + "empty_brackets.py",
                  "empty brackets test failed")

    def test_lone_import(self):
        """Test for lone import keyword"""
        pythonFile = self.dir + "loneimport.py"
        info = cdmpyparser.getBriefModuleInfoFromFile(pythonFile)
        if info.isOK:
            self.fail("lone import test failure. Expected error. Option: "
                      "directly from file: " + pythonFile)

        f = open(pythonFile)
        content = f.read()
        f.close()

        info = cdmpyparser.getBriefModuleInfoFromMemory(content)
        if info.isOK:
            self.fail("lone import test failure. Expected error. Option: "
                      "from memory. File: " + pythonFile)


# Run the unit tests
if __name__ == '__main__':
    print("Testing parser version: " + cdmpyparser.getVersion())
    print("Module location: " + cdmpyparser.__file__)
    unittest.main()
