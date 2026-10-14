from datetime import date as DateValue
from decimal import Decimal

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


class ExpenseCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    category: str = Field(min_length=1, max_length=100)
    date: DateValue | None = None
    payer_id: int
    person_id: int
    description: str | None = Field(default=None, max_length=1000)


class ExpenseAllocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

