from itertools import count
from bin.mongodb import mongo_client
from modules.common import crypt


def resolve_result():
    vote5 = list(mongo_client.db_get_collection("vote5").find())
    user3 = mongo_client.db_get_collection("user3")
    candidates_with_votes = []
    result_list = []
    for i in vote5:
        if i["value"] not in candidates_with_votes:
            candidates_with_votes.append(i["value"])
            candidate = user3.find_one({"_id": crypt.str_decrypt(i["value"])})
            result_list.append({
                "vote_id": i["value"],
                "candidate": candidate["party_name"],
                "count": 1
            })
        else:
            for j in result_list:
                if j["vote_id"] == i["value"]:
                    j["count"] += 1
    candidates_with_votes.clear()
    result_list.sort(key=lambda x: x["count"], reverse=True)
    return result_list
