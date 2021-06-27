from .core import Database


DEFAULT_PROJECTION = {"_id": False}


def get_user_info(db: Database):
    user_info = db.user_info.find_one({}, DEFAULT_PROJECTION)
    return user_info


def get_all_schemes(db: Database):
    schemes = db.schemes.find({}, DEFAULT_PROJECTION)
    return list(schemes)


def get_scheme(db: Database, amfi: str):
    data = db.schemes.find_one({"amfi": amfi}, DEFAULT_PROJECTION)
    return data


def get_user_goals(db: Database):
    return db.user_info.find_one(projection={**DEFAULT_PROJECTION, "goals": True})


def is_valid_goal(db: Database, goal: str):
    return db.user_info.count_documents({"goals": goal})
