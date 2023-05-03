from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    phone: str
    password: str
    roles: Union[str, None]


class UserLogin(UserBase):
    password: str


class TokenBase(BaseModel):
    username: str


class TokenCreate(TokenBase):
    token: str


class Token(TokenBase):
    token: str

    class Config:
        orm_mode = True


class ScoreBase(BaseModel):
    username: str


class ScoreCreate(ScoreBase):
    course: str
    score: int


class Score(ScoreBase):
    course: str
    score: int

    class Config:
        orm_mode = True


class User(UserBase):
    phone: str
    roles: str
    accessToken: str
    refreshToken: str
    expires: str
    is_active: bool

    token: List[Token] = []

    scores: List[Score] = []

    class Config:
        orm_mode = True
