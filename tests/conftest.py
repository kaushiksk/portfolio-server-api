import pytest
from portfolioserver import create_app
from portfolioserver.configs import TestingConfig
from portfolioserver.db import get_db

config = TestingConfig()


@pytest.fixture(scope="module")
def client():
    app = create_app(config)

    with app.test_client() as test_client:
        with app.app_context():
            init_db_for_test()
        yield test_client

    cleanup_db_after_test()


def init_db_for_test():
    db = get_db()
    db.user_info.insert_one({"_id": 1, "name": "Test User", "goals": ["goal1"]})


def cleanup_db_after_test():
    db = get_db()
    db.user_info.drop()
