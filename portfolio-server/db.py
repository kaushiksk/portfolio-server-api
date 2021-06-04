from flask.cli import with_appcontext
from flask_pymongo import PyMongo
from flask import current_app
from pyportfolio import Portfolio
from .codec_options import get_type_registry
import click
import cutie
import os
import sys

CAS_FILE_PATH = "./cas-portfolio.pdf"
mongo = PyMongo()


def get_db():
    return mongo.db


def init_app(app):
    mongo.init_app(app, type_registry=get_type_registry())
    app.cli.add_command(init_db_command)


@click.command("init-db")
@with_appcontext
def init_db_command():
    if not os.path.exists(CAS_FILE_PATH):
        print(
            "File not found. Make sure you saved your CAS file as cas-portfolio.pdf in directory root"
        )
        sys.exit(0)

    password = cutie.secure_input("Please enter the pdf password:")
    p = Portfolio(CAS_FILE_PATH, password)
    data = p.to_json()

    db = get_db()

    db.user_info.drop()
    db.schemes.drop()

    data["user_info"]["valuation"] = data["valuation"]
    for scheme in data["schemes"]:
        scheme["goal"] = "MISC"

    db.user_info.insert_one(data["user_info"])
    db.schemes.insert_many(data["schemes"])
