from fastapi import APIRouter, Depends
from .db import get_db
from .models import Portfolio
from .db.utils import get_all_schemes, get_user_info

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/overview", response_model=Portfolio)
def overview(db=Depends(get_db)):
    schemes = get_all_schemes(db)
    user_info = get_user_info(db)
    return Portfolio(user_info=user_info, schemes=schemes)
