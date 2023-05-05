#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(50, "lab 5-1 exception, Store/AMO page fault")
def test_exception_load():
    r.run_qemu(shell_script([
        'exceptest',
        'echo SUCCESS',
    ]))
    r.match('PID .* : Store/AMO page fault at .*', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


@test(50, "lab 5-1 exception, Load page fault")
def test_exception_store():
    r.run_qemu(shell_script([
        'exceptest',
        'echo SUCCESS',
    ]))
    r.match('PID .* : Load page fault at .*', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


run_tests()
