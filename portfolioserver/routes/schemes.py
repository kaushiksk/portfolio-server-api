from fastapi import APIRouter, Depends, HTTPException
from portfolioserver.db import get_db
from portfolioserver.models import (
    GoalRequest,
    GenericPostResponse,
    SchemeWithTransactions,
)
from portfolioserver.errors import INVALID_SCHEME, GOAL_NOT_FOUND
from portfolioserver.db.utils import get_scheme, is_valid_goal
from portfolioserver.db.crud import set_scheme_goal

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("/{amfi_id}/details", response_model=SchemeWithTransactions)
def scheme_details(amfi_id: str, db=Depends(get_db)):
    data = get_scheme(db, amfi_id)
    if not data:
        raise HTTPException(status_code=404, detail=INVALID_SCHEME)
    return data


@router.post("/{amfi_id}/assigngoal", response_model=GenericPostResponse)
def assign_goal(amfi_id: str, goal: GoalRequest, db=Depends(get_db)):
    response = GenericPostResponse()

    if is_valid_goal(db, goal.name):
        updated = set_scheme_goal(db, amfi_id, goal.name)
        if updated:
            response.isSuccess = True
        else:
            response.error = INVALID_SCHEME

    else:
        response.error = GOAL_NOT_FOUND

    return response
