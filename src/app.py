from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pyportfolio import Portfolio
from codec_options import get_codec_options
import cutie

CAS_FILE_PATH = "./cas-portfolio.pdf"

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/portfolio"

mongo = PyMongo(app)
db = mongo.db.with_options(codec_options=get_codec_options())


@app.route("/portfolio/overview/")
def index():
    _schemes = db.schemes.find(projection={"_id": False, "transactions": False})
    data = {"schemes": [s for s in _schemes]}
    return jsonify(data), 200


if __name__ == "__main__":
    import os
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Self Hosted API for your portfolio")
    parser.add_argument("--reload-db", default=False, action="store_true")
    parser.add_argument("--debug", default=False, action="store_true")

    args = parser.parse_args()

    if db.list_collection_names() == [] or args.reload_db:
        if not os.path.exists(CAS_FILE_PATH):
            print(
                "File not found. Make sure you saved your CAS file as cas-portfolio.pdf in current directory"
            )
            sys.exit(0)

        password = cutie.secure_input("Please enter the pdf password:")
        p = Portfolio(CAS_FILE_PATH, password)
        data = p.to_json()

        db.user_info.drop()
        db.schemes.drop()

        data["user_info"]["valuation"] = data["valuation"]
        for scheme in data["schemes"]:
            scheme["goal"] = "MISC"

        db.user_info.insert_one(data["user_info"])
        db.schemes.insert_many(data["schemes"])

    app.run("0.0.0.0", 5000, args.debug)
