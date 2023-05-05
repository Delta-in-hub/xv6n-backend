#!/usr/bin/env python3

import re
from gradelib import *

r = Runner()


@test(20, "running lazytest")
def test_lazytests():
    r.run_qemu(shell_script([
        'lazytest'
    ]))
    r.match("init: starting sh")


@test(20, "lazy: map", parent=test_lazytests)
def test_filetest():
    r.match("test lazy unmap: OK")


@test(20, "lazy: unmap", parent=test_lazytests)
def test_memtest():
    r.match("test lazy alloc: OK")

# test out of memory: OK


@test(20, "lazy: out of memory", parent=test_lazytests)
def test_memtest():
    r.match("test out of memory: OK")


@test(20, "lazy: forktest", parent=test_lazytests)
def test_memtest():
    r.run_qemu(shell_script([
        'forktest',
    ]))
    r.match("fork test OK")

#  usertests too much , cost too much time


run_tests()
