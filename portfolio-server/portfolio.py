from flask import Blueprint, jsonify
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
