from typing import List

import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import response
import schemas
import re
import os
from database import SessionLocal, engine
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/get/gradelib.py")
def getGradeLib():
    return FileResponse(path="./asset/gradelib.py", filename="gradelib.py", media_type='text/plain')


@router.get("/get/{lab_item}")
def getGradePy(lab_item: str):

    restr = r"lab[0-9]+-[0-9]+-?.*\.py"
    eng = re.compile(restr)
    if (eng.match(lab_item) == None):
        raise HTTPException(status_code=404, detail="Lab Name Not Found")

    if (os.path.exists(f"./asset/{lab_item}") == False):
        raise HTTPException(
            status_code=404, detail=f"File {lab_item} Not Found")

    return FileResponse(path=f"./asset/{lab_item}", filename=f"{lab_item}", media_type='text/plain')
