from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/portfolio"

    from . import db
    from . import portfolio
    from . import schemes

    db.init_app(app)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(schemes.bp)

    return app
