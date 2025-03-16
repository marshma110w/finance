from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship
from models.user import User, UserPublic
from models.expense_category import ExpenseCategory

class ExpenseBase(SQLModel):
    title: str = Field(index=True)
    text: str | None = Field(default=None)
    amount: Decimal = Field(decimal_places=2, ge=0)
    
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="expense_category.id")

class Expense(ExpenseBase, table=True):    
    """ Модель расхода для БД """
    id: int | None = Field(default=None, primary_key=True)
    
    user: User = Relationship(back_populates="expenses")
    category: ExpenseCategory = Relationship(back_populates="expenses")
    
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


class ExpensePublic(ExpenseBase):
    """ Модель для показа расхода """
    id: int
    category: ExpenseCategory


class ExpensePublicWithUser(ExpensePublic):
    user: UserPublic


class ExpenseCreate(ExpenseBase):
    """ Модель для создания расхода """
    pass


class ExpenseUpdate(ExpenseBase):
    """ Модель для обновления расхода """
    title: str | None = None
    text: str | None = None
    amount: Decimal | None = None
    user_id: int | None = None
