from typing import List

import bcrypt
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import reponse
import schemas
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


@router.post("/register", response_model=reponse.loginResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    res = reponse.loginResponse()
    if db_user:
        res.success = False
        return res
    db_user = crud.create_user(db=db, user=user)
    res.success = True
    res.data = schemas.User.from_orm(db_user)
    return res


@router.post("/login", response_model=reponse.loginResponse)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    res = reponse.loginResponse()
    if db_user:
        if check_password(user.password, db_user.hashed_password):
            res.success = True
            res.data = schemas.User.from_orm(db_user)
            return res
    res.success = False
    return res


if __name__ == "__main__":
    hashpwd = get_hashed_password("admin123")
    print("admin123", hashpwd)
    print(check_password("admin123", hashpwd))

    print("20194755pwd", get_hashed_password("20194755pwd"))
