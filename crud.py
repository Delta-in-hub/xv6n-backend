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


def refresh_token(db: Session, token: schemas.TokenCreate):
    db_token = db.query(models.UserToken).filter(
        models.UserToken.username == token.username).first()

    if db_token is None:
        db_token = models.UserToken(username=token.username, token=token.token)
        db.add(db_token)
    else:
        db_token.token = token.token

    db.commit()
    db.refresh(db_token)
    return db_token


def get_token(db: Session, username: str):
    db_token = db.query(models.UserToken).filter(
        models.UserToken.username == username).first()
    return db_token


def get_username_by_token(db: Session, token: str) -> str:
    db_token = db.query(models.UserToken).filter(
        models.UserToken.token == token).first()
    if db_token is None:
        return None
    return db_token.username


def updateScore(db: Session, userscore: schemas.ScoreCreate) -> models.Score:
    db_score = db.query(models.Score).filter(models.Score.username == userscore.username).filter(
        models.Score.course == userscore.course).first()
    if not db_score:
        db_score = models.Score(
            username=userscore.username, course=userscore.course, score=userscore.score)
        db.add(db_score)
    else:
        db_score.score = userscore.score
    db.commit()
    db.refresh(db_score)
    return db_score


def get_scores_by_labitem(db: Session, labitem: str):
    db_score = db.query(models.Score).filter(
        models.Score.course == labitem).all()
    return db_score
