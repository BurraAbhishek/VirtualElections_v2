from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from modules.voter.forms import VoterEditForm
from modules.election.voting_form import CastVote
from bin.mongodb import mongo_client
from modules.common import crypt


def user3_filter():
    user3 = mongo_client.db_get_collection("user3")
    user3_allowed = user3.find({"tosViolation": False})
    return list(user3_allowed)


def voter_screening(request):
    authorizationcollection = mongo_client.db_get_collection("mod2")
    authorization = authorizationcollection.find_one(
        {"_id": "access_control"}
    )
    if not authorization["canVote"]:
        raise PermissionDenied
    if request.method == "POST":
        auth = VoterEditForm(request.POST)
        if auth.is_valid():
            creds = mongo_client.db_get_collection("user4")
            voter_idtype = auth.cleaned_data["citype"]
            voter_id_value = auth.cleaned_data["cidno"]
            cred_id = creds.find_one({
                "identification": {
                    voter_idtype: voter_id_value
                }
            })
            cred_pass = cred_id["password"]
            u_pass = auth.cleaned_data["cpass"]
            if check_password(u_pass, cred_pass):
                voterid = crypt.str_encrypt(cred_id["_id"])
                votes = mongo_client.db_get_collection("vote5")
                vote = list(votes.find({"_id": voterid}))
                if len(vote) > 0:
                    raise PermissionDenied
                request.session["voter"] = cred_id["_id"]
                selected = user3_filter()
                selected.reverse()
                for i in selected:
                    i["id"] = i["_id"]
                return render(
                    request,
                    "election/castvote.html",
                    {
                        "form": CastVote,
                        "candidates": selected,
                        "submitlabel": "Save Changes"
                    }
                )
            else:
                return render(
                    request,
                    "voter/editlogin.html",
                    {
                        "form": VoterEditForm(),
                        "submitlabel": "Log In"
                    }
                )
        else:
            raise PermissionDenied
    else:
        return render(
            request,
            "election/editlogin.html",
            {
                "form": VoterEditForm(),
                "submitlabel": "Log In"
            }
        )
