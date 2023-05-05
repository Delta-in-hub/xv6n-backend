import os
import re
import uuid
from typing import List

import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import response
import schemas
from database import SessionLocal, engine

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def checkLabName(lab: str):
    restr = r"lab[0-9]+-[0-9]+-?.*"
    eng = re.compile(restr)
    if eng.match(lab) == None:
        return False
    if os.path.exists(f"./asset/{lab}.py") == False:
        return False
    return True


def getScoreLab_1_1(content: str) -> int:
    return 99


def getScoreLab_1_2(content: str) -> int:
    return 100


scoreReEng = re.compile(r"Score: ([0-9]+)/([0-9]+)")


def getScoreLab_2_1(content: str) -> int:
    res = scoreReEng.search(content)
    if not res:
        return 0
    return 100 * int(res.groups()[0]) // int(res.groups()[1])


# == Test lab2-1 hello world == lab2-1 hello world: OK (1.0s)
# Score: 100/100


LABTESTER = {
    "lab1-1": getScoreLab_1_1,
    "lab1-2": getScoreLab_1_2,
    "lab2-1-hello": getScoreLab_2_1,
    "lab2-2-find": getScoreLab_2_1,
    "lab2-3-getppid": getScoreLab_2_1,
    "lab2-4-getsched": getScoreLab_2_1,
    "lab3-1-pthread": getScoreLab_2_1,
    "lab3-2-sem": getScoreLab_2_1,
    "lab3-3-sem_impl": getScoreLab_2_1,
    "lab4-1-sched": getScoreLab_2_1,
    "lab4-2-mlfq": getScoreLab_2_1,
    "lab5-1-exception": getScoreLab_2_1,
    "lab5-2-minigdb": getScoreLab_2_1,
    "lab6-1-bestfit": getScoreLab_2_1,
    "lab6-2-buddy": getScoreLab_2_1,
    "lab6-3-umalloc": getScoreLab_2_1,
    "lab7-1-lazy": getScoreLab_2_1,
    "lab7-2-cow": getScoreLab_2_1,
    "lab8-1-symlink": getScoreLab_2_1,
    "lab8-2-largefile": getScoreLab_2_1,
    "lab8-3-mmap": getScoreLab_2_1,
}


@router.post("/handin")
def handinLab(res: schemas.TestUpload, db: Session = Depends(get_db)):
    username = crud.get_username_by_token(db, res.token)
    if not username:
        raise HTTPException(
            status_code=400, detail=f"Invalid token: {res.token}")
    if not checkLabName(res.lab):
        raise HTTPException(
            status_code=400, detail=f"Invalid lab name: {res.lab}")
    try:
        content = bytes.fromhex(res.content).decode('utf-8')
    except:
        raise HTTPException(
            status_code=400, detail=f"Invalid content: {res.content[:8]} ...")

    score = LABTESTER[res.lab](content)
    sc = schemas.ScoreCreate(username=username, course=res.lab, score=score)
    return crud.updateScore(db, sc)
