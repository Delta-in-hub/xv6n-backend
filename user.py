from typing import List

import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import response
import schemas
import uuid
from database import SessionLocal, engine


bcrypt_salt: bytes = b'$2b$04$x3xcAmNtOsDtEo/XRWcEfu'  # bcrypt.gensalt()


def get_hashed_password(plain_text_password: str):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password.encode(), bcrypt_salt).decode()


def check_password(plain_text_password: str, hashed_password: str):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password.encode())


# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/register", response_model=response.loginResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    res = response.loginResponse()
    if db_user or user.roles is None:
        res.success = False
        return res
    db_user = crud.create_user(db=db, user=user)
    res.success = True
    res.data = schemas.User.from_orm(db_user)
    return res

# update


@router.post("/updatepwd", response_model=response.loginResponse)
def update_password(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    res = response.loginResponse()
    if db_user:
        if db_user.phone == user.phone:
            db_user.hashed_password = get_hashed_password(user.password)
            db.commit()
            db.refresh(db_user)
            res.success = True
            res.data = schemas.User.from_orm(db_user)
            return res
    res.success = False
    return res


@router.post("/login", response_model=response.loginResponse)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    res = response.loginResponse()
    if db_user:
        if check_password(user.password, db_user.hashed_password):
            res.success = True
            res.data = schemas.User.from_orm(db_user)
            return res
    res.success = False
    return res


def generate_token(username: str) -> str:
    return f"{username}-{uuid.uuid4().hex}"


@router.get("/gettoken/{username}")
def getToken(username: str, db: Session = Depends(get_db)):
    db_token = crud.get_token(db, username)
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid username")
    return db_token


@router.post("/refreshtoken")
def refreshToken(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if not db_user:
        raise HTTPException(
            status_code=400, detail="Invalid username")
    tokenobj = schemas.TokenCreate(username=db_user.username,
                                   token=generate_token(db_user.username))
    return crud.refresh_token(db, tokenobj)


if __name__ == "__main__":
    hashpwd = get_hashed_password("admin123")
    print("admin123", hashpwd)
    print(check_password("admin123", hashpwd))

    print("20194755pwd", get_hashed_password("20194755pwd"))
