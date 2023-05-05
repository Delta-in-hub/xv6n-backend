#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(100, "getschedtime, test")
def test_getschedtime():
    r.run_qemu(shell_script([
        './getschedtimetest',
        'echo SUCCESS'
    ]))
    r.match('child .*')
    r.match('parent .*')


run_tests()
