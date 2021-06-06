from fastapi import APIRouter, Body, Depends
from .db import get_db

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/goals/", status_code=200)
def goals(_db=Depends(get_db)):
    user_goals = _db.user_info.find_one(projection={"goals": 1})
    return user_goals


@router.post("/goals/addgoal", status_code=201)
def addgoal(goal: str = Body(...), _db=Depends(get_db)):
    if goal is not None:
        _db.user_info.update_one({"_id": 1}, {"$addToSet": {"goals": goal}})
        return {"isSuccess": True}


@router.post("/goals/removegoal")
def removegoal(goal: str = Body(...), _db=Depends(get_db)):
    if goal is not None:
        is_valid_goal = _db.user_info.count_documents({"goals": goal})

        if is_valid_goal:
            schemes_with_goal = _db.schemes.count_documents({"goal": goal})

            if schemes_with_goal == 0:
                d = _db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal}})
                print(d.modified_count)
                return {"isSuccess": True}

            return {
                "error": "Cannot remove goal. There are schemes which have this goal assigned."
            }

        return {"error": "Cannot remove goal. Goal does not exist."}
