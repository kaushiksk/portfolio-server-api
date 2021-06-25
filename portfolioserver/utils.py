import json


def import_goals(goals_file, default_goal):
    goals = set([default_goal])
    scheme_mapping = {}

    goals_data = get_goals_data_from_file(goals_file)

    if goals_data:
        goals |= set(goals_data["goals"])

        for scheme in goals_data["schemes"]:
            scheme_mapping[scheme["amfi"]] = scheme["goal"]

    return list(goals), scheme_mapping


def get_goals_data_from_file(goals_file):
    if goals_file:
        try:
            with open(goals_file, "r") as file:
                goals_data = json.load(file)
                return goals_data
        except (EnvironmentError, json.JSONDecodeError):
            return None

    return None
