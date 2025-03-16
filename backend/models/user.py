from datetime import datetime
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    """ Базовая модель пользователя """
    telegram_id: int = Field(index=True, unique=True)
    name: str | None = Field(default=None)
    login: str | None = Field(default=None, unique=True)
    phone_number: str = Field(default=None, unique=True)


class User(UserBase, table=True):
    """ Модель пользователя для БД """
    id: int | None = Field(default=None, primary_key=True)

    expenses: list["Expense"] = Relationship(back_populates="user")  # type: ignore

    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True), onupdate=func.now(), nullable=True
        )
    )


class UserPublic(UserBase):
    """ Модель для показа пользователя """
    id: int

class UserCreate(UserBase):
    """ Модель для создания пользователя """
    pass

class UserUpdate(UserBase):
    """ Модель для обновления пользователя """
    telegram_id: int | None = None
    name: str | None = None
    login: str | None = None
    phone_number: str | None = None

