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


@router.get("/getAllScores/{username}")
def getAllScores(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=username)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f"User {username} not found")
    user = schemas.User.from_orm(db_user)
    return {"username": user.username, "scores": user.scores}


@router.get("/getAllStudentsScores")
def getAllStudentsScores(db: Session = Depends(get_db)):
    db_users = crud.get_users(db, skip=0, limit=100000)
    users = []
    for db_user in db_users:
        user = schemas.User.from_orm(db_user)
        users.append({"username": user.username, "scores": user.scores})
    return users
