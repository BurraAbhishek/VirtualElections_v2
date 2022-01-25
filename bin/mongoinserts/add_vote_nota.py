from bin.mongodb import mongo_client
from django.contrib.auth.hashers import make_password


nota_vote = {
    "_id": "00000000",
    "party_name": "None of the above",
    "candidate_name": "None of the above",
    "candidate_age": 50,
    "candidate_identification": {
        "NOTA_id": "00000000"
    },
    "password": make_password("00000000"),
    "showProfile": False,
    "isSymbolUploaded": False,
    "tosViolation": False
}


def add_nota():
    mongo_client.db_get_collection("user3").insert_one(nota_vote)
