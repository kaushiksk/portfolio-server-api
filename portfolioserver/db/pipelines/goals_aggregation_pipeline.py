step_1_group_by_type_and_subtype = {
    "$group": {
        "_id": {"goal": "$goal", "type": "$type", "subtype": "$subtype"},
        "subTypeCount": {"$sum": 1},
        "subTypeAmount": {"$sum": "$valuation"},
        "schemes": {
            "$push": {"amfi": "$amfi", "name": "$name", "valuation": "$valuation"}
        },
    }
}

step_2_sort_subtype_amount_desc = {"$sort": {"subTypeAmount": -1}}

step_3_group_by_type = {
    "$group": {
        "_id": {"goal": "$_id.goal", "type": "$_id.type"},
        "subtypes": {
            "$push": {
                "subtype": "$_id.subtype",
                "scheme_count": "$subTypeCount",
                "valuation": "$subTypeAmount",
                "schemes": "$schemes",
            }
        },
        "typeCount": {"$sum": "$subTypeCount"},
        "typeAmount": {"$sum": "$subTypeAmount"},
    }
}

step_4_sort_type_amount_desc = {"$sort": {"typeAmount": -1}}

step_5_group_by_goal = {
    "$group": {
        "_id": {"goal": "$_id.goal"},
        "types": {
            "$push": {
                "type": "$_id.type",
                "scheme_count": "$typeCount",
                "valuation": "$typeAmount",
                "subtypes": "$subtypes",
            }
        },
        "scheme_count": {"$sum": "$typeCount"},
        "valuation": {"$sum": "$typeAmount"},
    }
}

step_6_sort_valuation_desc = {"$sort": {"valuation": -1}}

step_7_project_result = {
    "$project": {
        "_id": 0,
        "goal": "$_id.goal",
        "stats": {
            "scheme_count": "$scheme_count",
            "valuation": "$valuation",
            "scheme_types": "$types",
        },
    }
}


GOALS_AGGREGATE_STATS_PIPELINE = [
    step_1_group_by_type_and_subtype,
    step_2_sort_subtype_amount_desc,
    step_3_group_by_type,
    step_4_sort_type_amount_desc,
    step_5_group_by_goal,
    step_6_sort_valuation_desc,
    step_7_project_result,
]


def get_matching_group_filter(goal: str):
    return [{"$match": {"goal": goal}}]


def get_goals_stats_pipeline(goal: str = None):
    if goal is None:
        return GOALS_AGGREGATE_STATS_PIPELINE

    return get_matching_group_filter(goal) + GOALS_AGGREGATE_STATS_PIPELINE
