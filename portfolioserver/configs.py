class DevelopmentConfig(object):
    MONGO_URI = "mongodb://localhost:27017/portfolio"
    DEFAULT_GOAL = "MISC"


class TestingConfig(object):
    MONGO_URI = "mongodb://localhost:27017/portfolio-test"
