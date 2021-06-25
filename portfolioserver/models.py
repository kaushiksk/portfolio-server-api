from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel as PydanticBaseModel
from decimal import Decimal
import locale

locale.setlocale(locale.LC_NUMERIC, "en_IN")


class BaseModel(PydanticBaseModel):
    class Config:
        json_encoders = {
            Decimal: lambda x: locale.format_string("%.4f", x, grouping=True)
        }


class GenericPostResponse(BaseModel):
    isSuccess: Optional[bool] = False
    error: Optional[str] = None


class GoalRequest(BaseModel):
    name: str


class Transaction(BaseModel):
    date: date
    description: str
    amount: Decimal
    units: Union[Decimal, None]
    nav: Union[Decimal, None]
    balance: Union[Decimal, None]
    type: str
    dividend_rate: Union[Decimal, None]
    days: int


class Scheme(BaseModel):
    amfi: str
    name: str
    units: Decimal
    nav: Decimal
    valuation: Decimal
    type: str
    subtype: str
    goal: str


class SchemeWithTransactions(Scheme):
    transactions: List[Transaction]


class GoalResponse(BaseModel):
    goals: List[str]


class UserInfo(BaseModel):
    name: str
    email: str
    address: str
    mobile: str
    valuation: Decimal
    goals: List[str]


class Portfolio(BaseModel):
    user_info: UserInfo
    schemes: List[Scheme]
