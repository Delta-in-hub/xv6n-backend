#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(100, "running bigfile")
def test_bigfile():
    r.run_qemu(shell_script([
        'bigfile'
    ]), timeout=400)
    r.match('^wrote 65803 blocks$')
    r.match('^bigfile done; ok$')


run_tests()
