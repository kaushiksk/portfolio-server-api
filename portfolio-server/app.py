from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/portfolio"

    from . import db
    from . import portfolio
    from . import scheme

    db.init_app(app)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(scheme.bp)

    return app
