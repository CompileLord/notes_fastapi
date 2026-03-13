from sqlalchemy import Integer, Text, String, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    role: Mapped[str] = mapped_column(String, default="user")
    password_hash: Mapped[str] = mapped_column(String)

    notes = relationship("Notes", back_populates="user")
    token = relationship("Token", back_populates="user")
    


class Notes(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, index=True, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notes")

class Token(Base):
    __tablename__ = 'tokens'

    id: Mapped[int] = mapped_column(Integer, index=True, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="token")

    