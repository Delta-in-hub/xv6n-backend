#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(0, "running cowtest")
def test_cowtest():
    r.run_qemu(shell_script([
        'cowtest'
    ]))


@test(30, "simple", parent=test_cowtest)
def test_simple():
    matches = re.findall("^simple: ok$", r.qemu.output, re.M)
    assert_equal(len(matches), 2, "Number of appearances of 'simple: ok'")


@test(30, "three", parent=test_cowtest)
def test_three():
    matches = re.findall("^three: ok$", r.qemu.output, re.M)
    assert_equal(len(matches), 3, "Number of appearances of 'three: ok'")


@test(20, "file", parent=test_cowtest)
def test_file():
    r.match('^file: ok$')


@test(20, "cow fork, fork test")
def test_forktest():
    r.run_qemu(shell_script([
        'forktest',
    ]))
    r.match("fork test OK")


run_tests()
