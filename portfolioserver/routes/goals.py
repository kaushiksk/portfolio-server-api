from typing import Optional
from portfolioserver.db.analytics import get_goals_stats
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from portfolioserver.db import get_db
from portfolioserver.models import (
    GoalRequest,
    GenericPostResponse,
    GoalResponse,
    GoalsExport,
)
from portfolioserver.errors import (
    CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA,
    CANNOT_REMOVE_GOAL_NOT_FOUND,
)
from portfolioserver.db.crud import add_user_goal, remove_user_goal
from portfolioserver.db.utils import get_user_goals, is_valid_goal, get_all_schemes
from portfolioserver.utils import create_export_file

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
    response = GenericPostResponse()

    if is_valid_goal(db, goal.name):
        removed = remove_user_goal(db, goal.name)
        if removed:
            response.isSuccess = True
        else:
            response.error = CANNOT_REMOVE_GOAL_EXISTS_IN_SCHEMA
    else:
        response.error = CANNOT_REMOVE_GOAL_NOT_FOUND

    return response


@router.get("/export", response_model=GoalsExport)
def export_goals(db=Depends(get_db)):
    user_goals = get_user_goals(db)
    schemes = get_all_schemes(db)

    output_data = GoalsExport(goals=user_goals["goals"], schemes=schemes)
    export_file = create_export_file(output_data.json(indent=4))

    return FileResponse(
        export_file, media_type="application/json", filename="goals.json"
    )


@router.get("/stats")
def goals_stats(goal: Optional[str] = None, db=Depends(get_db)):
    return get_goals_stats(db, goal)
