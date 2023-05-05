#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(40, "lab 4-2 mlfq, os running to shell")
def test_sched_timeslice():
    r.run_qemu(shell_script([
        'echo SUCCESS',
    ]))
    r.match('.*$.*', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


@test(60, "lab 4-2 mlfq, schedtest")
def test_sched_run():
    r.run_qemu(shell_script([
        'schedtest',
        "\n\n",
        'echo SUCCESS'
    ]))
    r.match('.*fib == 9227465.*', no=['exec .* failed'])
    r.match(".*SUCCESS.*")


run_tests()
