from flask import Blueprint, request
from .db import get_db

bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@bp.route("/goals/", methods=["GET"])
def goals():
    _db = get_db()
    user_goals = _db.user_info.find_one(projection={"goals": 1})
    return user_goals, 200


@bp.route("/goals/addgoal", methods=["POST"])
def addgoal():
    data = request.get_json()
    goal = data.get("goal", None)

    if goal is not None:
        _db = get_db()
        _db.user_info.update_one({"_id": 1}, {"$addToSet": {"goals": goal}})
        return {"isSuccess": True}, 200

    return {"error": "Json payload needs key 'goal'"}, 400


@bp.route("/goals/removegoal", methods=["POST"])
def removegoal():
    data = request.get_json()
    goal = data.get("goal", None)

    if goal is not None:
        _db = get_db()

        is_valid_goal = _db.user_info.count_documents({"goals": goal})

        if is_valid_goal:
            schemes_with_goal = _db.schemes.count_documents({"goal": goal})

            if schemes_with_goal == 0:
                d = _db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal}})
                print(d.modified_count)
                return {"isSuccess": True}, 200

            return {
                "error": "Cannot remove goal. There are schemes which have this goal assigned."
            }, 500

        return {"error": "Cannot remove goal. Goal does not exist."}, 500

    return {"error": "Json payload needs key 'goal'"}, 400
