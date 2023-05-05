#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(0, "running symlinktest")
def test_symlinktest():
    r.run_qemu(shell_script([
        'symlinktest'
    ]), timeout=20)


@test(45, "symlinktest: symlinks", parent=test_symlinktest)
def test_symlinktest_symlinks():
    r.match("^test symlinks: ok$")


@test(45, "symlinktest: concurrent symlinks", parent=test_symlinktest)
def test_symlinktest_symlinks():
    r.match("^test concurrent symlinks: ok$")


# forktest
@test(10, "symlinktest: fork test")
def test_forktest():
    r.run_qemu(shell_script([
        'forktest',
    ]))
    r.match("fork test OK")


run_tests()
