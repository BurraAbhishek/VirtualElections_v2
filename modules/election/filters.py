from bin.mongodb import mongo_client
from modules.common import age
from modules.common.shrug import is_shrug


def user3_filter() -> list:
    user3 = mongo_client.db_get_collection("user3")
    user3_allowed = user3.find({"tosViolation": False})
    return list(user3_allowed)


def age_filter(provisional: list) -> list:
    mod2 = mongo_client.db_get_collection("mod2")
    candidate_ages = mod2.find_one({"_id": "candidate_ages"})
    if not candidate_ages["boolRequired"]:
        return provisional
    else:
        min_age = candidate_ages["minAge"]
        max_age = candidate_ages["maxAge"]
        finalized = []
        for i in provisional:
            if i["_id"] == "00000000":
                finalized.append(i)
            else:
                if min_age <= i["candidate_age"] <= max_age:
                    finalized.append(i)
        return finalized


def is_voter(candidate) -> bool:
    user4 = mongo_client.db_get_collection("user4")
    id_dict = candidate["candidate_identification"]
    id_key = list(id_dict.keys())[0]
    if not is_shrug(id_key):
        return False
    id_value = id_dict[id_key]
    if not is_shrug(id_value):
        return False
    target = user4.find_one(
        {
            "identification": {
                id_key: id_value
            }
        }
    )
    if target is None:
        return False
    if candidate["candidate_name"] != target["name"]:
        return False
    if candidate["candidate_age"] != age.calculateAge(
        target["date_of_birth"][0],
        target["date_of_birth"][1],
        target["date_of_birth"][2]
    ):
        return False
    return True


def must_vote_filter(provisional: list) -> list:
    mod2 = mongo_client.db_get_collection("mod2")
    must_vote = mod2.find_one({"_id": "candidate_must_vote"})
    if not must_vote["boolValue"]:
        return provisional
    else:
        finalized = []
        for i in provisional:
            if i["_id"] == "00000000":
                finalized.append(i)
            elif is_voter(i):
                finalized.append(i)
        return finalized


def is_candidate_qualified(candidate_id: str) -> bool:
    mod2 = mongo_client.db_get_collection("mod2")
    user3 = mongo_client.db_get_collection("user3")
    user3_voted = user3.find_one({"_id": candidate_id})
    if user3_voted["tosViolation"] is True:
        return False
    must_vote = mod2.find_one({"_id": "candidate_must_vote"})
    if must_vote["boolValue"]:
        if not is_voter(user3_voted):
            return False
    candidate_ages = mod2.find_one({"_id": "candidate_ages"})
    if candidate_ages["boolRequired"]:
        min_age = candidate_ages["minAge"]
        max_age = candidate_ages["maxAge"]
        if min_age <= user3_voted["candidate_age"] <= max_age:
            return False
    return True
