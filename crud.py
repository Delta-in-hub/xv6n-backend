from sqlalchemy.orm import Session

import models
import schemas
import user as userpart


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    _hashed_password = userpart.get_hashed_password(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=_hashed_password, phone=user.phone)
    db_user.roles = user.roles

    # hard code the token for convenience
    db_user.accessToken = "eyJhbGciOiJIUzUxMiJ9."+user.username
    db_user.refreshToken = "eyJhbGciOiJIUzUxMiJ9."+user.username+"Refresh"
    db_user.expires = "2023/10/30 00:00:00"
    # accessToken: "eyJhbGciOiJIUzUxMiJ9.admin",
    # refreshToken: "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
    # expires: "2023/10/30 00:00:00"

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# admin123notreallyhashed
