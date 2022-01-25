from bin.mongodb import mongo_client

access_controls = {
    "_id": "access_control",
    "canVotersRegister": True,
    "canContestantsRegister": True,
    "canVote": True,
    "canShowResults": True
}


candidate_privacy_restrictions = {
    "_id": "candidate_privacy",
    "views": "Default",
    "showTosViolation": "True"
}


def add_access_controls():
    mongo_client.db_insert_one(
        collection="mod2",
        data=access_controls
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=candidate_privacy_restrictions
    )
