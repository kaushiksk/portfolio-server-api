from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/portfolio"

    from . import db

    db.init_app(app)

    from . import portfolio

    app.register_blueprint(portfolio.bp)

    return app
