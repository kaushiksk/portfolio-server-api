from .core import Database
from .pipelines import get_goals_stats_pipeline


def get_goals_stats(db: Database, goal: str = None):
    result = db.schemes.aggregate(get_goals_stats_pipeline(goal))
    return list(result)
