from fastapi import APIRouter, Body, Depends
from .db import get_db

router = APIRouter(prefix="/schemes", tags=["schemes"])


@router.get("/overview")
def overview(_db=Depends(get_db)):
    _schemes = _db.schemes.find(projection={"_id": False, "transactions": False})
    user_info = _db.user_info.find_one({})
    data = {"user_info": user_info, "schemes": [s for s in _schemes]}
    return data, 200


@router.get("/{amfi_id}")
def scheme_details(amfi_id: str, _db=Depends(get_db)):
    data = _db.schemes.find_one_or_404({"amfi": amfi_id}, projection={"_id": False})
    return data, 200


@router.post("/{amfi_id}/assigngoal")
async def assigngoal(amfi_id: str, goal: str = Body(...), _db=Depends(get_db)):
    is_valid_scheme = _db.schemes.count_documents({"amfi": amfi_id})

    if not is_valid_scheme:
        return {"error": "Invalid Scheme"}

    if goal is not None:
        is_valid_goal = _db.user_info.count_documents({"goals": goal})

        if is_valid_goal:
            _db.schemes.update_one({"amfi": amfi_id}, {"$set": {"goal": goal}})
            return {"isSuccess": True}

        return {"error": "Provided goal is not part of user's goals. Add it first."}

    return {"error": "Json payload needs key 'goal'"}
