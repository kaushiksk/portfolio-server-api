from .core import Database


def set_scheme_goal(db: Database, amfi: str, goal: str) -> bool:
    result = db.schemes.update_one({"amfi": amfi}, {"$set": {"goal": goal}})
    return result.matched_count == 1


def add_user_goal(db: Database, goal: str):
    db.user_info.update_one({"_id": 1}, {"$addToSet": {"goals": goal}})


def remove_user_goal(db: Database, goal: str) -> bool:
    schemes_with_goal = db.schemes.count_documents({"goal": goal.name})

    if schemes_with_goal == 0:
        db.user_info.update_one({"_id": 1}, {"$pull": {"goals": goal.name}})
        return True

    return False
