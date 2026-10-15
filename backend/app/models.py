from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.expense_distribution import calculate_debts


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    invitation_code: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
    )


class BoardMembership(Base):
    __tablename__ = "board_memberships"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"),
        primary_key=True,
    )


class MonthlyBudget(Base):
    __tablename__ = "monthly_budgets"

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"),
        primary_key=True,
    )
    year: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[int] = mapped_column(primary_key=True)
    available_base: Mapped[Decimal] = mapped_column(Numeric(14, 2))


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100))


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    category: Mapped[str] = mapped_column(String(100))
    date: Mapped[date] = mapped_column(Date)
    payer_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    expense_type: Mapped[str] = mapped_column(String(20), default="personal")
    allocations: Mapped[list["ExpenseAllocation"]] = relationship(
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="ExpenseAllocation.participant_id",
    )

    @property
    def debts(self) -> list[dict[str, int | Decimal]] | None:
        debts = calculate_debts(
            payer_id=self.payer_id,
            allocations=[
                (allocation.participant_id, allocation.amount)
                for allocation in self.allocations
            ],
        )
        if not debts:
            return None
        return [
            {"participant_id": participant_id, "amount": amount}
            for participant_id, amount in debts
        ]


class ExpenseAllocation(Base):
    __tablename__ = "expense_allocations"

    expense_id: Mapped[int] = mapped_column(
        ForeignKey("expenses.id"),
        primary_key=True,
    )
    participant_id: Mapped[int] = mapped_column(
        ForeignKey("participants.id"),
        primary_key=True,
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2))

