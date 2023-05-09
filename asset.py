from typing import List

import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy.orm import Session
import shutil
import crud
import models
import response
import schemas
import re
import os
from database import SessionLocal, engine
from fastapi.responses import FileResponse


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/get/gradelib.py")
def getGradeLib():
    return FileResponse(path="./asset/gradelib.py", filename="gradelib.py", media_type='text/plain')


@router.get("/get/example_release.json")
def getExampleRelease():
    return FileResponse(path="./asset/example_release.json", filename="example_release.json", media_type='text/json')


def checkLabName(lab_item: str):
    if not lab_item.endswith(".py"):
        lab_item += ".py"
    restr = r"lab[0-9]+-[0-9]+-?.*\.py"
    eng = re.compile(restr)
    if (eng.match(lab_item) == None):
        return False
    if (os.path.exists(f"./asset/{lab_item}") == False):
        return False
    return True


@router.get("/get/{lab_item}")
def getGradePy(lab_item: str):
    if not lab_item.endswith(".py"):
        lab_item += ".py"
    if (checkLabName(lab_item) == False):
        raise HTTPException(
            status_code=404, detail=f"File {lab_item} Not Found --")

    return FileResponse(path=f"./asset/{lab_item}", filename=f"{lab_item}", media_type='text/plain')


@router.post("/uploadcode/{token}/{lab_item}")
def uploadCode(token: str, lab_item: str, code: UploadFile, db: Session = Depends(get_db)):
    username = crud.get_username_by_token(db, token)
    if not username:
        raise HTTPException(
            status_code=404, detail=f"{token} Not Found")
    if (checkLabName(lab_item) == False):
        raise HTTPException(
            status_code=404, detail=f"Lab {lab_item} Not Found")
    if not code.filename.endswith(".tar.gz"):
        raise HTTPException(
            status_code=400, detail=f"File {code.filename} is not a tar.gz file")
    # write file to ./asset/stucodes/{username}/{lab_item}.tar.gz
    try:
        if not os.path.exists(f"./asset/stucodes/{username}"):
            os.mkdir(f"./asset/stucodes/{username}")
        with open(f"./asset/stucodes/{username}/{lab_item}.tar.gz", "wb") as f:
            shutil.copyfileobj(code.file, f)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{e}")
    finally:
        code.file.close()
    return {"status": "upload code tar.gz ok"}


@router.get("/getcode/{username}/{lab_item}")
def getCode(username: str, lab_item: str, db: Session = Depends(get_db)):
    if crud.get_user_by_name(db, username) == None:
        raise HTTPException(
            status_code=404, detail=f"User {username} Not Found")
    if (checkLabName(lab_item) == False):
        raise HTTPException(
            status_code=404, detail=f"File {lab_item} Not Found")
    if (os.path.exists(f"./asset/stucodes/{username}/{lab_item}.tar.gz") == False):
        raise HTTPException(
            status_code=404, detail=f"File {lab_item} Not Found")
    return FileResponse(path=f"./asset/stucodes/{username}/{lab_item}.tar.gz", filename=f"{lab_item}.tar.gz", media_type='application/x-gzip')
