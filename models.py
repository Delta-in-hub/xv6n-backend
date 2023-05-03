from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, primary_key=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    #     username: "admin",
    # roles: ["admin"],
    # accessToken: "eyJhbGciOiJIUzUxMiJ9.admin",
    # refreshToken: "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
    # expires: "2023/10/30 00:00:00"
    roles = Column(String)  # admin / common
    accessToken = Column(String)
    refreshToken = Column(String)
    expires = Column(String)
    is_active = Column(Boolean, default=True)

    token = relationship("UserToken", back_populates="owner")
    scores = relationship("Score", back_populates="owner")


class UserToken(Base):
    __tablename__ = "users_token"
    token = Column(String, nullable=False, primary_key=True)
    username = Column(String, ForeignKey("users.username"), index=True)
    owner = relationship("User", back_populates="token")


class Score(Base):
    __tablename__ = "scores"

    username = Column(String, ForeignKey("users.username"), primary_key=True)
    course = Column(String, primary_key=True)
    score = Column(Integer)

    owner = relationship("User", back_populates="scores")
