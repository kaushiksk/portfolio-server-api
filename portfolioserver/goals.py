from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from .db import get_db
from .models import GoalRequest, GenericPostResponse, GoalResponse, GoalsExport
from .errors import CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA, CANNOT_REMOVE_GOAL_NOT_FOUND

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/", status_code=200, response_model=GoalResponse)
def goals(_db=Depends(get_db)):
    user_goals = _db.user_info.find_one(projection={"_id": False, "goals": True})
    return user_goals


@router.post("/addgoal", status_code=201, response_model=GenericPostResponse)
def add_goal(goal: GoalRequest, _db=Depends(get_db)):
    _db.user_info.update_one({"_id": 1}, {"$addToSet": {"goals": goal.name}})
    return GenericPostResponse(isSuccess=True)


@router.post("/removegoal", response_model=GenericPostResponse)
def remove_goal(goal: GoalRequest, _db=Depends(get_db)):
    is_valid_goal = _db.user_info.count_documents({"goals": goal.name})

    if is_valid_goal:
        schemes_with_goal = _db.schemes.count_documents({"goal": goal.name})

        if schemes_with_goal == 0:
            _db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal.name}})
            return GenericPostResponse(isSuccess=True)

        return GenericPostResponse(error=CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA)

    return GenericPostResponse(error=CANNOT_REMOVE_GOAL_NOT_FOUND)


@router.get("/export", response_model=GoalsExport)
def export_goals(_db=Depends(get_db)):
    user_goals = _db.user_info.find_one(projection={"_id": False, "goals": True})
    scheme_goals = _db.schemes.find(
        {}, projection={"_id": False, "amfi": True, "goal": True}
    )

    schemes = [s for s in scheme_goals]
    output_data = GoalsExport(goals=user_goals["goals"], schemes=schemes)

    import tempfile

    with tempfile.NamedTemporaryFile("w", delete=False) as file:
        file.write(output_data.json(indent=4))
        return FileResponse(
            file.name, media_type="application/json", filename="goals.json"
        )
