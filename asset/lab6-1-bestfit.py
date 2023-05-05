#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(50, "lab 6-1 bestfit, pass ktest and run to shell")
def test_exception_load():
    r.run_qemu(shell_script([
        'echo SUCCESS',
    ]))
    r.match('ktest: cpu.* pass all tests', no=['exec .* failed'])
    r.match("init: starting sh")
    r.match(".*SUCCESS.*")


@test(50, "lab 6-2 bestfit, fork need alloc memory")
def test_exception_store():
    r.run_qemu(shell_script([
        'forktest',
        'echo SUCCESS',
    ]))
    r.match('fork test OK', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


run_tests()


# ktest: cpu1 pass all tests
