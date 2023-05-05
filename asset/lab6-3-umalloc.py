
#! /usr/bin/env python3

import subprocess
from subprocess import Popen
from grade import safeRemove


def pthread_test():
    try:
        proc = Popen(["./_umalloc_test"], stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

        content = ""
        while proc.stdout.readable():
            line = proc.stdout.readline()
            if len(line) == 0:
                break
            print(line.decode('utf-8'), end='')
            content += line.decode('utf-8')
        proc.wait()
    except Exception as e:
        print(e)

    return content


def getScore(content: str) -> int:
    if (content == None or len(content) == 0):
        return 0
    try:
        if "umalloc works as expected!" in content:
            return 100
    except:
        return 0

    return 100

# umalloc works as expected!


if __name__ == "__main__":
    content = pthread_test()
    score = getScore(content)
    print("== Test umalloc == user space memory allocation ")
    print(f"Score: {score}/100")
    safeRemove("_umalloc_test")


# _umalloc_test
