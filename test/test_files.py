import os

import FilesCheck
from FilesCheck import python_bytecode_to_script as pbts
from FilesCheck import script_interpreter as se
import Testing


class TestPythonBytecodeToScript(object):

    def test_pep3147(self):
        assert pbts("/usr/lib64/python3.4/__pycache__/__phello__.foo.cpython-34.pyc") == "/usr/lib64/python3.4/__phello__.foo.py"
        assert pbts("/usr/lib64/python3.4/__pycache__/__phello__.foo.cpython-34.pyo") == "/usr/lib64/python3.4/__phello__.foo.py"

    def test_py2(self):
        assert pbts("/usr/lib/python2.7/site-packages/_pytest/main.pyc") == "/usr/lib/python2.7/site-packages/_pytest/main.py"
        assert pbts("/usr/lib/python2.7/site-packages/_pytest/main.pyo") == "/usr/lib/python2.7/site-packages/_pytest/main.py"

    def test_pep0488(self):
        assert pbts("/usr/lib/python3.5/site-packages/__pycache__/pytest.cpython-35.opt-1.pyc") == "/usr/lib/python3.5/site-packages/pytest.py"
        assert pbts("/usr/lib/python3.5/site-packages/__pycache__/pytest.cpython-35.opt-2.pyc") == "/usr/lib/python3.5/site-packages/pytest.py"
        assert pbts("/usr/lib/python3.5/site-packages/__pycache__/pytest.cpython-35.pyc") == "/usr/lib/python3.5/site-packages/pytest.py"


class TestPythonBytecodeMagic(Testing.OutputTest):

    @classmethod
    def setup_class(cls):
        cls.check = FilesCheck.check.check

    def test_python_bytecode_magic(self):
        for package in ["python3-power"]:
            out = self._rpm_test_output(os.path.join("binary", package))
            assert "python-bytecode-wrong-magic-value" not in "\n".join(out)


def test_script_interpreter():
    assert se(b"#!/bin/sh\n# Hello world!\n") == ("/bin/sh", "")
    assert se(b"#!/bin/bash -e\n") == ("/bin/bash", "-e")
    assert se(b"#! /usr/bin/perl -wT \n") == ("/usr/bin/perl", "-wT")
    assert se(b"#!/usr/bin/env python3 foo") == ("/usr/bin/env", "python3 foo")
    assert se(b"# something here\n#!not a shebang") == (None, "")
