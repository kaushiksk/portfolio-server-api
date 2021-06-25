from .core import Database


def get_user_info(db: Database):
    user_info = db.user_info.find_one({}, projection={"_id": False})
    return user_info


def get_all_schemes(db: Database):
    schemes = db.schemes.find({}, projection={"_id": False})
    return [s for s in schemes]


def get_scheme(db: Database, amfi: str):
    data = db.schemes.find_one({"amfi": amfi}, projection={"_id": False})
    return data


def get_user_goals(db: Database):
    return db.user_info.find_one(projection={"_id": False, "goals": True})


def is_valid_goal(db: Database, goal: str):
    return db.user_info.count_documents({"goals": goal})
