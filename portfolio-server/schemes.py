from flask import Blueprint, request
from .db import get_db

bp = Blueprint("schemes", __name__, url_prefix="/schemes")


@bp.route("/overview/", methods=["GET"])
def overview():
    _db = get_db()
    _schemes = _db.schemes.find(projection={"_id": False, "transactions": False})
    user_info = _db.user_info.find_one({})
    data = {"user_info": user_info, "schemes": [s for s in _schemes]}
    return data, 200


@bp.route("/<amfi_id>", methods=["GET"])
def scheme_details(amfi_id):
    _db = get_db()
    data = _db.schemes.find_one_or_404({"amfi": amfi_id}, projection={"_id": False})
    return data, 200


@bp.route("/<amfi_id>/assigngoal", methods=["POST"])
def assigngoal(amfi_id):
    _db = get_db()
    _db.schemes.find_one_or_404({"amfi": amfi_id})

    data = request.get_json()
    goal = data.get("goal", None)

    if goal is not None:
        is_valid_goal = _db.user_info.count_documents({"goals": goal})

        if is_valid_goal:
            _db.schemes.update_one({"amfi": amfi_id}, {"$set": {"goal": goal}})
            return {"isSuccess": True}, 200

        return {
            "error": "Provided goal is not part of user's goals. Add it first."
        }, 400

    return {"error": "Json payload needs key 'goal'"}, 400
