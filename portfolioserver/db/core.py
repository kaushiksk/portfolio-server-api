from pymongo import MongoClient
from pymongo.database import Database
from pyportfolio import Portfolio
from portfolioserver.configs import DevelopmentConfig
from .codec_options import get_type_registry
from portfolioserver.utils import import_goals
import cutie


app_config = DevelopmentConfig()


def get_mongo_client(config=None):
    if config is None:
        config = app_config

    mongo = MongoClient(config.MONGO_URI, type_registry=get_type_registry())
    return mongo


mongo = get_mongo_client()


def get_db() -> Database:
    return mongo.get_default_database()


def init_db_from_cas_file(cas_file_path, goals_file=None):
    password = cutie.secure_input("Please enter the pdf password:")
    p = Portfolio(cas_file_path, password)
    data = p.to_json()

    db = get_db()

    db.user_info.drop()
    db.schemes.drop()

    data["user_info"]["valuation"] = data["valuation"]
    data["user_info"]["_id"] = 1

    goals, scheme_mapping = import_goals(goals_file, app_config.DEFAULT_GOAL)
    data["user_info"]["goals"] = goals
    for scheme in data["schemes"]:
        scheme["goal"] = scheme_mapping.get(scheme["amfi"], app_config.DEFAULT_GOAL)

    db.user_info.insert_one(data["user_info"])
    db.schemes.insert_many(data["schemes"])
