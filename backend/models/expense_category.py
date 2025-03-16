from sqlmodel import SQLModel, Field, Relationship
from typing import List

class ExpenseCategoryBase(SQLModel):
    __tablename__ = "expense_category"

    name: str = Field(index=True, unique=True)


class ExpenseCategory(ExpenseCategoryBase, table=True):

    """ Модель категории расходов для БД """
    id: int | None = Field(default=None, primary_key=True)

    expenses: List["Expense"] = Relationship(back_populates="category")  # type: ignore


class ExpenseCategoryPublic(ExpenseCategoryBase):
    """ Модель для показа категории расходов """
    id: int
