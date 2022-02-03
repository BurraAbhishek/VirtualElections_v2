from bin.mongodb import mongo_client
from modules.common import crypt


def gender_turnout():
    turnout = mongo_client.db_get_collection("turnout")
    vote5 = mongo_client.db_get_collection("vote5").find()
    user_vote5 = []
    gender_total = {
        "_id": "gender_all",
        "Male": 0,
        "Female": 0,
        "Other": 0,
        "Total": 0
    }
    gender_composition = {
        "_id": "gender_composition",
        "Male": 0,
        "Female": 0,
        "Other": 0,
        "Total": 0
    }
    for i in vote5:
        user_vote5.append(crypt.str_decrypt(i["_id"]))
    user4 = mongo_client.db_get_collection("user4").find()
    for i in user4:
        gender_total[i["gender"]] += 1
        gender_total["Total"] += 1
        if i["_id"] in user_vote5:
            gender_composition[i["gender"]] += 1
            gender_composition["Total"] += 1
    try:
        turnout.insert_one(gender_total)
    except:
        turnout.update_one(
            {
                '_id': "gender_all"
            },
            {
                "$set": {
                    'Male': gender_total["Male"],
                    'Female': gender_total["Female"],
                    'Other': gender_total["Other"],
                    'Total': gender_total["Total"]
                }
            }
        )
    try:
        turnout.insert_one(gender_composition)
    except:
        turnout.update_one(
            {
                '_id': "gender_composition"
            },
            {
                "$set": {
                    'Male': gender_composition["Male"],
                    'Female': gender_composition["Female"],
                    'Other': gender_composition["Other"],
                    'Total': gender_composition["Total"]
                }
            }
        )


def recompute_result():
    user5 = mongo_client.db_get_collection("user5")
    user5.drop()
    vote5 = list(mongo_client.db_get_collection("vote5").find())
    user3 = mongo_client.db_get_collection("user3")
    candidates_with_votes = []
    result_list = []
    for i in vote5:
        if i["value"] not in candidates_with_votes:
            candidates_with_votes.append(i["value"])
            candidate = user3.find_one({"_id": crypt.str_decrypt(i["value"])})
            result_list.append({
                "_id": i["value"],
                "candidate": crypt.str_encrypt(candidate["party_name"]),
                "count": 1
            })
        else:
            for j in result_list:
                if j["_id"] == i["value"]:
                    j["count"] += 1
    candidates_with_votes.clear()
    result_list.sort(key=lambda x: x["count"], reverse=True)
    user5 = mongo_client.db_get_collection("user5")
    for i in result_list:
        user5.insert_one(i)
    return result_list


def resolve_result():
    user5 = mongo_client.db_get_collection("user5")
    user5_list = list(user5.find())
    for i in user5_list:
        i["candidate"] = crypt.str_decrypt(i["candidate"])
    return user5_list
