#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(50, "lab 5-2 minigdb, breakpoint at ...")
def test_exception_load():
    r.run_qemu(shell_script([
        'exceptest',
        'echo SUCCESS',
    ]))
    r.match('PID .* : Breakpoint at 0x0000000000000020', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


@test(50, "lab 5-2 minigdb, after ebreak")
def test_exception_store():
    r.run_qemu(shell_script([
        'exceptest',
        'echo SUCCESS',
    ]))
    r.match('.*93.*fd.*a8.*3b.*e7.*23.*80', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


run_tests()
