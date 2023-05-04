#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(35, "find, in current directory")
def test_find_curdir():
    fn = random_str()
    r.run_qemu(shell_script([
        'echo > %s' % fn,
        'find . %s' % fn
    ]))
    r.match('./%s' % fn)


@test(65, "find, recursive")
def test_find_recursive():
    needle = random_str()
    dirs = [random_str() for _ in range(3)]
    r.run_qemu(shell_script([
        'mkdir %s' % dirs[0],
        'echo > %s/%s' % (dirs[0], needle),
        'mkdir %s/%s' % (dirs[0], dirs[1]),
        'echo > %s/%s/%s' % (dirs[0], dirs[1], needle),
        'mkdir %s' % dirs[2],
        'echo > %s/%s' % (dirs[2], needle),
        'find . %s' % needle
    ]))
    r.match('./%s/%s' % (dirs[0], needle),
            './%s/%s/%s' % (dirs[0], dirs[1], needle),
            './%s/%s' % (dirs[2], needle))


run_tests()
