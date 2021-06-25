from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from .db import get_db
from .models import GoalRequest, GenericPostResponse, GoalResponse, GoalsExport
from .errors import CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA, CANNOT_REMOVE_GOAL_NOT_FOUND
from .db.crud import add_user_goal, remove_user_goal
from .db.utils import get_user_goals, is_valid_goal, get_all_schemes
from .utils import create_export_file

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/", status_code=200, response_model=GoalResponse)
def goals(db=Depends(get_db)):
    user_goals = get_user_goals(db)
    return user_goals


@router.post("/addgoal", status_code=201, response_model=GenericPostResponse)
def add_goal(goal: GoalRequest, db=Depends(get_db)):
    add_user_goal(db, goal.name)
    return GenericPostResponse(isSuccess=True)


@router.post("/removegoal", response_model=GenericPostResponse)
def remove_goal(goal: GoalRequest, db=Depends(get_db)):
    if is_valid_goal(db, goal.name):
        removed = remove_user_goal(db, goal.name)
        if removed:
            return GenericPostResponse(isSuccess=True)

        return GenericPostResponse(error=CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA)

    return GenericPostResponse(error=CANNOT_REMOVE_GOAL_NOT_FOUND)


@router.get("/export", response_model=GoalsExport)
def export_goals(db=Depends(get_db)):
    user_goals = get_user_goals(db)
    schemes = get_all_schemes(db)

    output_data = GoalsExport(goals=user_goals["goals"], schemes=schemes)
    export_file = create_export_file(output_data.json(indent=4))

    return FileResponse(
        export_file, media_type="application/json", filename="goals.json"
    )
