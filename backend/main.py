from fastapi import FastAPI, Depends, HTTPException, Query
from logging import Logger
from sqlmodel import SQLModel, create_engine, Session, select

from typing import Annotated

from models.expense import Expense, ExpenseCreate, ExpensePublic, ExpensePublicWithUser, ExpenseUpdate
from models.user import User, UserCreate, UserPublic, UserUpdate


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

# User paths
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

# Expense paths
@app.post("/expenses/", response_model=ExpensePublic)
def create_expense(expense: ExpenseCreate, session: SessionDep):
    db_expense = Expense.model_validate(expense)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.get("/expenses/", response_model=list[ExpensePublic])
def read_expenses(
    session: SessionDep,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    expenses = session.exec(select(Expense).offset(offset).limit(limit)).all()
    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpensePublicWithUser)
def read_expense(expense_id: int, session: SessionDep):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return expense

@app.get("/users/{user_id}/expenses/", response_model=list[ExpensePublic])
def get_user_expenses(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    expenses = session.exec(select(Expense).filter(Expense.user_id == user_id)).all()
    return expenses

@app.patch("/expenses/{expense_id}", response_model=ExpensePublic)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    session: SessionDep,
):
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expense_data = expense.model_dump(exclude_unset=True)
    db_expense.sqlmodel_update(expense_data)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, session: SessionDep):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    session.delete(expense)
    session.commit()
    return {"ok": True}
