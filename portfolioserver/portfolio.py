from fastapi import APIRouter, Depends
from .db import get_db
from .models import Portfolio

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/overview", response_model=Portfolio)
def overview(_db=Depends(get_db)):
    _schemes = [
        s for s in _db.schemes.find(projection={"_id": False, "transactions": False})
    ]
    user_info = _db.user_info.find_one({}, projection={"_id": False})
    return Portfolio(user_info=user_info, schemes=_schemes)
