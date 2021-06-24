from fastapi import APIRouter, Depends, HTTPException
from .db import get_db
from .models import GoalRequest, GenericPostResponse, SchemeWithTransactions, Portfolio
from .errors import INVALID_SCHEME, GOAL_NOT_FOUND

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("/overview", response_model=Portfolio)
def overview(_db=Depends(get_db)):
    _schemes = [s for s in _db.schemes.find(projection={"_id": False, "transactions": False})]
    user_info = _db.user_info.find_one({}, projection={"_id": False})
    return Portfolio(user_info=user_info, schemes=_schemes)


@router.get("/{amfi_id}", response_model=SchemeWithTransactions)
def scheme_details(amfi_id: str, _db=Depends(get_db)):
    data = _db.schemes.find_one({"amfi": amfi_id}, projection={"_id": False})
    if not data:
        raise HTTPException(status_code=404, detail=INVALID_SCHEME) 
    return data


@router.post("/{amfi_id}/assigngoal", response_model=GenericPostResponse)
async def assign_goal(amfi_id: str, goal: GoalRequest, _db=Depends(get_db)):
    is_valid_scheme = _db.schemes.count_documents({"amfi": amfi_id})

    if not is_valid_scheme:
        raise HTTPException(status_code=404, detail=INVALID_SCHEME) 

    is_valid_goal = _db.user_info.count_documents({"goals": goal.name})

    if is_valid_goal:
        _db.schemes.update_one({"amfi": amfi_id}, {"$set": {"goal": goal.name}})
        return GenericPostResponse(isSuccess=True)

    return GenericPostResponse(error=GOAL_NOT_FOUND)