from fastapi import FastAPI


def create_app():
    app = FastAPI()

    from . import portfolio
    from . import schemes

    app.include_router(portfolio.router)
    app.include_router(schemes.router)

    return app
