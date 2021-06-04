from flask import Blueprint, jsonify
from .db import get_db

bp = Blueprint("scheme", __name__, url_prefix="/scheme")


@bp.route("/<amfi_id>/details/", methods=["GET"])
def scheme_details(amfi_id):
    _db = get_db()
    data = _db.schemes.find_one_or_404({"amfi": amfi_id}, projection={"_id": False})
    return data, 200
