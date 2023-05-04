#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(100,"lab2-1 hello world")
def test_hello_world():
    r.run_qemu(shell_script([
        './hello'
    ]))
    r.match("Hello World",no=["exec .* failed"])


run_tests()
