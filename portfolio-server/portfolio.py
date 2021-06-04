from flask import Blueprint, jsonify
from .db import get_db

bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@bp.route("/overview/", methods=["GET"])
def overview():
    _db = get_db()
    _schemes = _db.schemes.find(projection={"_id": False, "transactions": False})
    data = {"schemes": [s for s in _schemes]}
    return data, 200
