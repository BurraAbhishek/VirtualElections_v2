from bin.mongodb import mongo_client

access_controls = {
    "_id": "access_control",
    "canVotersRegister": True,
    "canContestantsRegister": True,
    "canVote": True,
    "canShowResults": True
}


election_type = {
    "_id": "election_type",
    "allow_local": True
}


candidate_privacy_restrictions = {
    "_id": "candidate_privacy",
    "views": "Default",
    "showTosViolation": True
}


candidate_vote = {
    "_id": "candidate_must_vote",
    "boolValue": False
}


voter_age_constraints = {
    "_id": "voter_ages",
    "boolRequired": False,
    "minAge": 0,
    "maxAge": 100,
}


candidate_age_constraints = {
    "_id": "candidate_ages",
    "boolRequired": False,
    "minAge": 0,
    "maxAge": 100,
}


def add_access_controls():
    mongo_client.db_insert_one(
        collection="mod2",
        data=access_controls
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=election_type
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=candidate_privacy_restrictions
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=voter_age_constraints
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=candidate_age_constraints
    )
    mongo_client.db_insert_one(
        collection="mod2",
        data=candidate_vote
    )
