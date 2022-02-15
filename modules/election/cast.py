from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from modules.election.voting_form import CastVote
from bin.mongodb import mongo_client
from modules.common.shrug import is_shrug
from modules.common import crypt
from modules.election.filters import is_candidate_qualified


def successfully_voted(request) -> render:
    return render(
        request,
        "oops/security_closepage.html",
        {
            "success_text": "Your vote was successfully cast",
            "success_message": " ".join(
                [
                    "Your vote was successfully cast.",
                    "This means that you voted successfully."
                ]
            )
        }
    )


def process_vote(request, vote_candidate_id):
    vote5 = mongo_client.db_get_collection("vote5")
    voter = request.session["voter"]
    encoded_vote = {
        "_id": crypt.str_encrypt(voter),
        "value": crypt.str_encrypt(vote_candidate_id),
    }
    vote5.insert_one(encoded_vote)


def cast_vote(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canVote"]:
        raise PermissionDenied
    if request.method == "POST":
        vote = CastVote(request.POST)
        if vote.is_valid():
            vote_candidate_id = str(vote.cleaned_data["party_id"])
            if is_shrug(vote_candidate_id):
                user3 = mongo_client.db_get_collection("user3")
                if not is_candidate_qualified(vote_candidate_id):
                    raise PermissionDenied
                else:
                    process_vote(request, vote_candidate_id)
                    request.session.__delitem__("voter")
                    return successfully_voted(request)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied
