import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient
from portfolioserver import create_app
from portfolioserver.configs import TestingConfig
from portfolioserver.db import get_db, get_mongo_client

config = TestingConfig()
mongo_test = get_mongo_client(config)


def get_test_db():
    return mongo_test.get_default_database()


app = create_app()
app.dependency_overrides[get_db] = get_test_db
test_client = TestClient(app)


@pytest.fixture(scope="module")
def client():
    init_db_for_test()
    yield test_client
    cleanup_db_after_test()


def init_db_for_test():
    db = get_test_db()
    db.user_info.insert_one({"_id": 1, "name": "Test User", "goals": ["goal1"]})


def cleanup_db_after_test():
    db = get_test_db()
    db.user_info.drop()
