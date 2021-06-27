from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel as PydanticBaseModel
from decimal import Decimal
from fastapi.encoders import jsonable_encoder


def decimal_encoder(number: Decimal):
    """We want to round the decimal to 4 decimal places
    and return the value with default encoding used by FastAPI
    """
    rounded_number = number.quantize(Decimal(".0001"))
    return jsonable_encoder(rounded_number)


class BaseModel(PydanticBaseModel):
    class Config:
        json_encoders = {Decimal: decimal_encoder}


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


class SchemeGoal(BaseModel):
    amfi: str
    goal: str


class GoalsExport(BaseModel):
    goals: List[str]
    schemes: List[SchemeGoal]


class BaseAggregation(BaseModel):
    scheme_count: int
    valuation: Decimal


class SchemeName(BaseModel):
    amfi: str
    name: str


class SchemeSubTypeAggregation(BaseAggregation):
    subtype: str
    schemes: List[SchemeName]


class SchemeTypeAggregation(BaseAggregation):
    type: str
    subtypes: List[SchemeSubTypeAggregation]


class GoalStats(BaseAggregation):
    scheme_types: List[SchemeTypeAggregation]


class GoalAggregation(BaseModel):
    goal: str
    stats: GoalStats
