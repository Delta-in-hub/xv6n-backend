#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(30, "lab 4-1 sched viewer, going to run on CPU (ID)")
def test_sched_run():
    r.run_qemu(shell_script([
        'schedtest',
        'echo SUCCESS'
    ]))
    r.match('.*Pid .* is going to run on CPU .*', no=['exec .* failed'])
    r.match(".*SUCCESS.*")

# Pid 3 is going to run on CPU 2
# Pid 3 is yield on CPU 2, for waitting I/O
# Pid 7 is yield on CPU 1, for running out of time slice


@test(30, "lab 4-1 sched viewer, waitting I/O")
def test_sched_io():
    r.run_qemu(shell_script([
        'schedtest',
        'echo SUCCESS'
    ]))
    r.match('.*Pid .* is yield on CPU .*, for waitting I/O.*',
            no=['exec .* failed'])
    r.match(".*SUCCESS.*")


@test(40, "lab 4-1 sched viewer, time slice")
def test_sched_timeslice():
    r.run_qemu(shell_script([
        'schedtest',
        'echo SUCCESS'
    ]))
    r.match('.*Pid .* is yield on CPU .*, for running out of time slice.*',
            no=['exec .* failed'])
    r.match(".*SUCCESS.*")


run_tests()
