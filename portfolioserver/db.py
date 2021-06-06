from pymongo import MongoClient
from pyportfolio import Portfolio
from .configs import DevelopmentConfig
from .codec_options import get_type_registry
import click
import cutie
import os
import sys

config = DevelopmentConfig()
mongo = MongoClient(config.MONGO_URI, type_registry=get_type_registry())


def get_db():
    return mongo.get_default_database()


def init_db_from_cas_file(cas_file_path):
    password = cutie.secure_input("Please enter the pdf password:")
    p = Portfolio(cas_file_path, password)
    data = p.to_json()

    db = get_db()

    db.user_info.drop()
    db.schemes.drop()

    data["user_info"]["valuation"] = data["valuation"]
    data["user_info"]["_id"] = 1

    # TODO: Allow user to import goals
    data["user_info"]["goals"] = ["MISC"]
    for scheme in data["schemes"]:
        scheme["goal"] = "MISC"

    db.user_info.insert_one(data["user_info"])
    db.schemes.insert_many(data["schemes"])
