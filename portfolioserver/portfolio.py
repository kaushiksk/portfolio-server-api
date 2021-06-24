from fastapi import APIRouter, Body, Depends
from .db import get_db
from .models import GoalRequest, Portfolio, GenericPostResponse
from .errors import CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA, CANNOT_REMOVE_GOAL_NOT_FOUND

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/overview", response_model=Portfolio)
def overview(_db=Depends(get_db)):
    _schemes = [
        s for s in _db.schemes.find(projection={"_id": False, "transactions": False})
    ]
    user_info = _db.user_info.find_one({}, projection={"_id": False})
    return Portfolio(user_info=user_info, schemes=_schemes)


@router.get("/goals/", status_code=200)
def goals(_db=Depends(get_db)):
    user_goals = _db.user_info.find_one(projection={"goals": 1})
    return user_goals


@router.post("/goals/addgoal", status_code=201, response_model=GenericPostResponse)
def addgoal(goal: GoalRequest, _db=Depends(get_db)):
    _db.user_info.update_one({"_id": 1}, {"$addToSet": {"goals": goal.name}})
    return GenericPostResponse(isSuccess=True)


@router.post("/goals/removegoal", response_model=GenericPostResponse)
def removegoal(goal: GoalRequest, _db=Depends(get_db)):
    is_valid_goal = _db.user_info.count_documents({"goals": goal.name})

    if is_valid_goal:
        schemes_with_goal = _db.schemes.count_documents({"goal": goal.name})

        if schemes_with_goal == 0:
            _db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal.name}})
            return GenericPostResponse(isSuccess=True)

        return GenericPostResponse(error=CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA)

    return GenericPostResponse(error=CANNOT_REMOVE_GOAL_NOT_FOUND)
