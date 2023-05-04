#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(20, "getppid, makes syscall")
def test_sleep():
    r.run_qemu(shell_script([
        './getppidtest',
        'echo FAIL'
    ]), stop_breakpoint('sys_getppid'))
    r.match('\\$ ./getppidtest', no=['FAIL'])


@test(80, "run getppidtest and check the result")
def test_mmaptest():
    r.run_qemu(shell_script([
        './getppidtest'
    ]), timeout=180)
    r.match('getppidtest PASS', no=['ERROR.*'])


run_tests()
