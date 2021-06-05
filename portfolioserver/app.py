from flask import Flask
from .configs import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig())

    from . import db
    from . import portfolio
    from . import schemes

    db.init_app(app)
    app.register_blueprint(portfolio.bp)
    app.register_blueprint(schemes.bp)

    return app
