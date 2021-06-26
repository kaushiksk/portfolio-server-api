from fastapi import APIRouter, Depends, HTTPException
from .db import get_db
from .models import GoalRequest, GenericPostResponse, SchemeWithTransactions
from .errors import INVALID_SCHEME, GOAL_NOT_FOUND
from .db.utils import get_scheme, is_valid_goal
from .db.crud import set_scheme_goal

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
        result = set_scheme_goal(db, amfi_id, goal.name)
        if result.matched_count == 0:
            response.error = INVALID_SCHEME
        else:
            response.isSuccess = True
    else:
        response.error = GOAL_NOT_FOUND

    return response
