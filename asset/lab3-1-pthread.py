#! /usr/bin/env python3

import subprocess
from subprocess import Popen
from grade import safeRemove


def pthread_test():
    try:
        proc = Popen(["./_pthreadtest"], stdout=subprocess.PIPE,
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
        all = content.split('\n')
        for (i, line) in enumerate(all):
            if len(line) < 3:
                continue
            if i % 2 == 0:
                if line.split(" ")[0] not in ['Dad', 'Mom']:
                    return 0
            else:
                if line.split(" ")[0] not in ['Son', 'Daughter']:
                    return 0
    except:
        return 0

    return 100


if __name__ == "__main__":
    content = pthread_test()
    score = getScore(content)
    print("== Test pthread == producer and consumer ")
    print(f"Score: {score}/100")
    safeRemove("_pthreadtest")
