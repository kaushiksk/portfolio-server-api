from fastapi import FastAPI


def create_app():
    app = FastAPI()

    from . import portfolio
    from . import schemes
    from . import goals

    app.include_router(portfolio.router)
    app.include_router(schemes.router)
    app.include_router(goals.router)

    return app
