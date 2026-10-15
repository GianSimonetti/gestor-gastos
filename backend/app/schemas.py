from datetime import date as DateValue
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BoardCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)


class BoardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class InvitationCodeResponse(BaseModel):
    invitation_code: str


class JoinBoardRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    invitation_code: str = Field(min_length=1, max_length=32)


class ParticipantCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)


class ParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    name: str


class MonthlyBudgetSet(BaseModel):
    available_base: Decimal = Field(ge=0, max_digits=14, decimal_places=2)


class MonthlySummaryResponse(BaseModel):
    board_id: int
    year: int
    month: int
    available_base: Decimal
    consumed: Decimal
    remaining: Decimal


class ExpenseAllocationCreate(BaseModel):
    participant_id: int
    amount: Decimal = Field(ge=0, max_digits=14, decimal_places=2)


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    category: str = Field(min_length=1, max_length=100)
    date: DateValue | None = None
    payer_id: int
    expense_type: Literal["personal", "equal", "custom"] = "personal"
    person_id: int | None = None
    participant_ids: list[int] | None = None
    allocations: list[ExpenseAllocationCreate] | None = None
    description: str | None = Field(default=None, max_length=1000)


class ExpenseAllocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    participant_id: int
    amount: Decimal


class ExpenseDebtResponse(BaseModel):
    participant_id: int
    amount: Decimal


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    board_id: int
    name: str
    amount: Decimal
    category: str
    date: DateValue
    payer_id: int
    description: str | None
    expense_type: str
    allocations: list[ExpenseAllocationResponse]
    debts: list[ExpenseDebtResponse] | None = Field(
        default=None,
        exclude_if=lambda value: value is None,
    )

