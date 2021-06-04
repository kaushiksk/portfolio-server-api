from flask import Blueprint, request
from .db import get_db

bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@bp.route("/overview/", methods=["GET"])
def overview():
    _db = get_db()
    _schemes = _db.schemes.find(projection={"_id": False, "transactions": False})
    user_info = _db.user_info.find_one({})
    data = {"user_info": user_info, "schemes": [s for s in _schemes]}
    return data, 200


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

        schemes_with_goal = _db.schemes.count_documents({"goal": goal})

        if schemes_with_goal == 0:
            _db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal}})
            return {"isSuccess": True}, 200

        return {
            "error": "Cannot remove goal. There are schemes which have this goal assigned."
        }, 500

    return {"error": "Json payload needs key 'goal'"}, 400
