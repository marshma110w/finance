from fastapi import FastAPI, Depends, HTTPException
from logging import Logger
from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Annotated
from sqlalchemy import Column, DateTime, func


DATABASE_URL = "sqlite:///database.db"

logger = Logger(__name__)

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("End of lifespan")

app = FastAPI(lifespan=lifespan)

class UserBase(SQLModel):
    """ Базовая модель пользователя """
    telegram_id: int = Field(index=True, unique=True)
    name: str | None = Field(default=None)
    login: str | None = Field(default=None, unique=True)
    phone_number: str = Field(default=None, unique=True)


class User(UserBase, table=True):
    """ Модель пользователя для БД """
    id: int | None = Field(default=None, primary_key=True)
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


@app.post("/users", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserPublic])
def get_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    return user

@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"ok": True}
